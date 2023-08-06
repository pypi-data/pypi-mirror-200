"""
Manages the version number for the project based on git tags.
If on a tag, report that as-is.
When moved on from the tag, auto-increment the desired level of semantic version
"""
import re
import os
import sys
import tempfile
import argparse
import setuptools
import subprocess
from pathlib import Path
import traceback


# Set environment variable "VERSION_INCREMENT" to set next version jump
VERSION_INCREMENT_ENV = "VERSION_INCREMENT"

PROJECT_ROOT_ENV = "PROJECT_ROOT"

VERSION_INCREMENT_PATCH = 'patch'
VERSION_INCREMENT_MINOR = 'minor'
VERSION_INCREMENT_MAJOR = 'major'

SUPPORT_PATCH = os.environ.get("VERSION_SUPPORT_PATCH", False)

repo_dir = os.environ.get(PROJECT_ROOT_ENV, '.')


VERBOSE = False

# These are the main attributes tracked by git-versioner
version = "0.0-new"
version_short = "0.0.0" if SUPPORT_PATCH else "v0.0"
git_hash = ''
on_tag = False
dirty = True
version_py = "0.0+new"
version_py_short = "0.0"


# Load snapshot of attributes if one exists
try:
    from _version import version, version_short, git_hash, on_tag, dirty, SUPPORT_PATCH
    ignore_missing_git = True
except:
    ignore_missing_git = False


__git_safe_directory_cfg = None


def __git_safe_directory():
    global __git_safe_directory_cfg
    if os.geteuid() == 0:
        # running as root, likely inside container. Allow git to read repos from other users.

        if not __git_safe_directory_cfg:
            real_gitconfig_file = Path(os.environ.get("GIT_CONFIG_GLOBAL", Path.home() / ".gitconfig"))
            __git_safe_directory_cfg = tempfile.NamedTemporaryFile(prefix=".gitconfig_")
            if real_gitconfig_file.exists():
                __git_safe_directory_cfg.write(real_gitconfig_file.read_bytes())
                __git_safe_directory_cfg.flush()

            os.environ["GIT_CONFIG_GLOBAL"] = __git_safe_directory_cfg.name
            subprocess.check_output(["git", "config", "--global", "--add", "safe.directory", "*"])


__git_safe_directory()


def vers_split(vers):
    try:
        return list(re.search(r"v?(\d+\.\d+(\.\d+)?)", vers).group(1).split('.'))
    except:
        print("Could not parse version from:", vers, file=sys.stderr)
        raise


def get_version_info_from_git():
    global SUPPORT_PATCH
    fail_ret = None, None, None, None, True
    # Note: git describe doesn't work if no tag is available
    current_commit = None
    try:
        current_commit = subprocess.check_output(["git","rev-parse", "--short", "HEAD"],
                                          cwd=repo_dir, stderr=subprocess.STDOUT, universal_newlines=True).strip()
        git_describe = subprocess.check_output(["git", "describe", "--long", "--tags", "--dirty", "--always"],
                                          cwd=repo_dir, stderr=subprocess.STDOUT, universal_newlines=True).strip()
    except subprocess.CalledProcessError as er:
        if VERBOSE:
            traceback.print_exc()
        if er.returncode == 128:
            # git exit code of 128 means no repository found
            return fail_ret
        git_describe = ""
    except OSError:
        if VERBOSE:
            traceback.print_exc()
        return fail_ret

    if git_describe.startswith(current_commit):
        # No tags yet, new repo
        git_hash = current_commit
        parts = re.match(r'(^[a-f0-9]*?)(-dirty)?$', git_describe.lower())
        git_dirty = parts.group(2)
        tag_name = ""
        if SUPPORT_PATCH:
            git_tag_parts = ['0', '0', '0']
        else:
            git_tag_parts = ['0', '0']
        on_tag = False

    else:
        desc_parts = re.match(r'(^.*?)-(\d+)-g([a-f0-9]+?)(-dirty)?$', git_describe)
        tag_name = desc_parts.group(1)
        num_commits = desc_parts.group(2)
        git_hash = desc_parts.group(3)
        git_dirty = desc_parts.group(4)

        git_tag_parts = vers_split(git_describe)

        if len(git_tag_parts) == 3:
            SUPPORT_PATCH = True

        try:
            # Find all tags on the commit and get the largest version if there are multiple
            tag_sha = subprocess.check_output(["git", "rev-list", "-n", "1", tag_name],
                                              cwd=repo_dir, stderr=subprocess.STDOUT, universal_newlines=True).strip()

            sha_tags = subprocess.check_output(["git", "tag", "--points-at", tag_sha],
                                               cwd=repo_dir, stderr=subprocess.STDOUT, universal_newlines=True).strip()

            sha_tags = {tuple(vers_split(t)):t for t in sha_tags.split('\n')}
            git_tag_parts = max(sha_tags)
            tag_name = sha_tags[git_tag_parts]

        except subprocess.CalledProcessError as er:
            if VERBOSE:
                traceback.print_exc()

        except OSError:
            if VERBOSE:
                traceback.print_exc()
            return fail_ret

        on_tag = tag_name if tag_sha.startswith(git_hash) else False

    return list(git_tag_parts), tag_name, git_hash, on_tag, git_dirty


def increment_index(increment):
    try:
        index = {
            VERSION_INCREMENT_PATCH: 2,
            VERSION_INCREMENT_MINOR: 1,
            VERSION_INCREMENT_MAJOR: 0,
        }[increment]
    except KeyError:
        raise SystemExit("change: %s must be one of '%s', '%s' or '%s'" %
                         (increment, VERSION_INCREMENT_MAJOR,
                          VERSION_INCREMENT_MINOR, VERSION_INCREMENT_PATCH))
    return index


def increment_from_messages(tag_name):
    # Increment version
    increment = []

    # Check git logs between last tag and now
    try:
        git_range = "%s..HEAD" % tag_name if tag_name else "HEAD"
        commit_messages = subprocess.check_output(["git", "log", git_range],
                                cwd=repo_dir, stderr=subprocess.STDOUT, universal_newlines=True).strip()
    except subprocess.CalledProcessError:
        commit_messages = ''

    for match in re.findall(r'CHANGE: *(%s|%s|%s)' % (
        VERSION_INCREMENT_MAJOR, VERSION_INCREMENT_MINOR, VERSION_INCREMENT_PATCH
    ), commit_messages):
        try:
            increment.append(increment_index(match))
        except SystemExit as ex:
            print(ex.args, file=sys.stderr)
    if increment:
        return min(increment)
    return None


def git_version():
    global SUPPORT_PATCH
    parts, tag_name, g_hash, on_tag, dirty = get_version_info_from_git()
    if not parts:
        if ignore_missing_git:
            raise ResourceWarning()
        raise SystemExit("Error: Could not read git repo commit / details")
    try:
        if not (on_tag and not dirty):

            index = increment_from_messages(tag_name)

            # Fallback to checking env for increment if commit messages don't specify
            if index is None:
                increment = os.environ.get(VERSION_INCREMENT_ENV, VERSION_INCREMENT_MINOR).lower()
                index = increment_index(increment)
            if len(parts) < 2:
                if VERBOSE:
                    print("Adding minor version to scheme that previously had only major", file=sys.stderr)
                parts.append('0')
            if len(parts) < 3 and (
                SUPPORT_PATCH or
                index == increment_index(VERSION_INCREMENT_PATCH)
            ):
                if VERBOSE:
                    print("Adding patch version to scheme that is currently only <major>.<minor>", file=sys.stderr)
                SUPPORT_PATCH = True
                parts.append('0')

            max_index = 2 if SUPPORT_PATCH else 1

            parts = parts[0:index] + [str(int(parts[index]) + 1)] + (['0'] * max(0, (max_index - index)))

    except (IndexError, ValueError, AttributeError) as ex:
        if "'NoneType' object has no attribute 'group'" in str(ex):  # regex fail
            print("Parsing version number failed:", tag_name, file=sys.stderr)
        else:
            print("Could not increment %s : %s" % (tag_name, ex), file=sys.stderr)

    vers_short = "v" + ".".join(parts)
    if on_tag and not dirty:
        vers_long = on_tag
    else:
        vers_long = vers_short + '-g' + g_hash
        if dirty:
            vers_long += "-dirty"

    return vers_short, vers_long, g_hash, on_tag, dirty


def py_version():
    global version

    pv_short = version_short.lstrip("v")

    if on_tag and not dirty:
        local_parts = []
        match = re.search(r"v?\d+\.\d+(\.\d+)?(.*)$", version)
        if match:
            local = match.group(2).lstrip("-_")
            if local:
                local_parts.append(local)
    else:
        local_parts = ["g" + git_hash]

    if dirty and not local_parts[-1].endswith("-dirty"):
        local_parts.append("dirty")

    vers = pv_short
    if local_parts:
        vers = "+".join((vers, ".".join(local_parts)))

    # normalise the version to suitable package version
    try:
        from setuptools.extern import packaging
        vers = str(packaging.version.Version(vers))
    except:
        pass

    return vers, pv_short


def save(dest=None):
    import json
    dest = dest or Path(repo_dir)
    if dest.is_dir():
        dest /= '_version.py'
    dest.write_text(
        '# Version managed by git-versioner\n'
        f'version = "{version}"\n'
        f'version_short = "{version_short}"\n'
        f'git_hash = "{git_hash}"\n'
        f'on_tag = {repr(on_tag)}\n'
        f'dirty = {True if dirty else False}\n'
        f'SUPPORT_PATCH = {True if SUPPORT_PATCH else False}\n'
    )


def rename_file(pattern, short):
    global version, version_short
    import glob
    for f in glob.glob(pattern):
        f = Path(f)
        newname = f.name.format(
            version=version,
            version_short=version_short,
            git_hash=git_hash,
        )
        if newname == f.name:
            name, ext = f.stem, f.suffix
            newname = f"{name}-{version_short if short else version}{ext}"
        print(f'Renaming "{f}" -> "{newname}"')
        f.rename(f.with_name(newname))


def fill_file(template_file, output_file):
    template_file = Path(template_file)
    output_file = Path(output_file)
    template = template_file.read_text()
    output = template.format(
            version=version,
            version_short=version_short,
            git_hash=git_hash,
        )
    output_file.write_text(output)
    print("Written:", output_file)


## Set the global version values
error = None

# Check for static vars in env first
if any((key for key in os.environ if key.startswith("GIT_VERSIONER"))):
    def parse_bool_str(v):
        return (
            True if v.lower() in ["true", "1"] else
            False if v.lower() in ["false", "0", ""] else
            v
        )

    version = os.environ.get("GIT_VERSIONER_VERSION", version)
    version_short = os.environ.get("GIT_VERSIONER_VERSION_SHORT", version_short)
    git_hash = os.environ.get("GIT_VERSIONER_GIT_HASH", git_hash)
    on_tag = parse_bool_str(os.environ.get("GIT_VERSIONER_ON_TAG", repr(on_tag)))
    dirty = parse_bool_str(os.environ.get("GIT_VERSIONER_DIRTY", repr(dirty)))
    version_py = os.environ.get("GIT_VERSIONER_VERSION_PY", version_py)
    version_py_short = os.environ.get("GIT_VERSIONER_VERSION_PY_SHORT", version_py_short)
else:
    try:
        version_short, version, git_hash, on_tag, dirty = git_version()
    except ResourceWarning:
        pass
    except Exception as ex:
        error = str(ex)

    version_py, version_py_short = py_version()


def setup_keyword(dist: setuptools.Distribution, keyword, value):
    global version_py, version_py_short, setuptools
    if not value:
        return

    # setuptools command to save a static __version__.py in the build package
    class VersionCommand(setuptools.Command):
        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            build = self.distribution.command_obj.get('build')
            if build and self.distribution.packages:
                for package in self.distribution.packages:
                    dest = Path(build.build_lib) / package
                    if dest.exists():
                        save(dest / "__version__.py")

            sdist = self.distribution.command_obj.get('sdist')
            if sdist and sdist.filelist:
                save()
                sdist.filelist.files.append("_version.py")


    command = 'git-versioner'
    try:
        import pkg_resources
        command += ":" + pkg_resources.get_distribution("git-versioner").version
    except:
        pass

    dist.cmdclass[command] = VersionCommand

    # set the package version
    dist.metadata.version = version_py

    if "sdist" in dist.script_args:
        try:
            from setuptools.command import sdist
        except ImportError:
            from distutils.command import sdist
        sdist.sdist.sub_commands.append((command, None))

    # Cache the version in env for isolated builds
    if not any((key for key in os.environ if key.startswith("GIT_VERSIONER"))):
        os.environ["GIT_VERSIONER_VERSION"] = version
        os.environ["GIT_VERSIONER_VERSION_SHORT"] = version_short
        os.environ["GIT_VERSIONER_GIT_HASH"] = git_hash
        os.environ["GIT_VERSIONER_ON_TAG"] = repr(on_tag)
        os.environ["GIT_VERSIONER_DIRTY"] = "True" if dirty else "False"
        os.environ["GIT_VERSIONER_VERSION_PY"] = version_py
        os.environ["GIT_VERSIONER_VERSION_PY_SHORT"] = version_py_short

    # Handle options
    if not isinstance(value, str):
        return

    if "snapshot" in value:
        try:
            from setuptools.command import build
        except ImportError:
            from distutils.command import build
        build.build.sub_commands.append((command, None))

    if "desc" in value:
        # function can be run multiple times, ensure we only append once.
        if not dist.metadata.long_description.strip().endswith(version_py):
            dist.metadata.long_description += f"\n\nversion: {version_py}"

    if "gitlab" in value:
        # Long (PEP440 local) number schemes aren't allowed on PyPI
        # This scheme uses short version when building from default branch
        # or on tags.
        ci_commit_tag = os.environ.get("CI_COMMIT_TAG")
        if ci_commit_tag:
            dist.metadata.version = version_py_short
            return
        try:
            ci_commit_branch = os.environ.get("CI_COMMIT_BRANCH")
            ci_default_branch = os.environ["CI_DEFAULT_BRANCH"]
            if ci_commit_branch == ci_default_branch:
                dist.metadata.version = version_py_short
        except KeyError:
            # No env CI_DEFAULT_BRANCH, not running in Gitlab CI.
            pass

    elif "short" in value:
        dist.metadata.version = version_py_short


def main():
    global version, version_short, git_hash, on_tag, dirty, VERBOSE

    parser = argparse.ArgumentParser(description='Mange current/next version.')
    parser.add_argument('--save', action='store_true', help='Store in _version.py')
    parser.add_argument('--short', action='store_true', help='Print the short version string')
    parser.add_argument('--git', action='store_true', help='Print the release git hash')
    parser.add_argument('--python', action='store_true', help='display the python formatted version strings')
    parser.add_argument('--rename', help='Add version numbers to filename(s)')
    parser.add_argument('--template', metavar=('template', 'output'), type=Path, nargs=2,
                        help='Add version to <template> and write result to <output>')
    parser.add_argument('--tag', action='store_true', help='Creates git tag to release the current commit')
    parser.add_argument('--verbose', action='store_true', help='provide more detail on error')
    args = parser.parse_args()

    VERBOSE = args.verbose

    if error:
        # if there was an error during initial processing
        # above, try re-running it here.
        try:
            version_short, version, git_hash, on_tag, dirty = git_version()
        except:
            import traceback
            traceback.print_exc()
    if args.save:
        save()

    if args.rename:
        rename_file(args.rename, args.short)
        return
    if args.template:
        fill_file(args.template[0], args.template[1])
        return

    if args.tag:
        if on_tag:
            raise SystemExit("Already on tag", on_tag)
        if dirty:
            raise SystemExit("Git dirty, cannot tag")
        print(version_short)
        subprocess.run(["git", "tag", version_short], cwd=repo_dir)

    if args.short:
        if args.python:
            print(version_py_short)
        else:
            print(version_short)
    elif args.git:
        print(git_hash)
    else:
        if args.python:
            print(version_py)
        else:
            print(version)


if __name__ == "__main__":
    main()

if __git_safe_directory_cfg:
    __git_safe_directory_cfg.close()
