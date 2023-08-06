import argparse

import sys
import os
import shutil
from pathlib import Path
import fileinput
import yaml
import platform
import stat

def replace_in_file(path:str, ori:str, replace:str):
    with fileinput.FileInput(path, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(ori, replace), end='')
    os.remove(path+'.bak')

def replace_in_dir(directory:str, ori:str, replace:str):
    files = os.listdir(directory)
    for file in files:
        cur_path = os.path.join(directory, file)
        if os.path.isdir(cur_path):
            replace_in_dir(cur_path, ori, replace)
        else:
            replace_in_file(cur_path, ori, replace)

def find_target(directory:str, target:str) ->bool:
    files = os.listdir(directory)
    for file in files:
        if file == target:
            return True

    return False

def build_native(conanfile:str, chn:str, compiler:str, compilerVersion:str, archs:list, debug:bool, addition_settings:str=''):
    osName=platform.system()
    match osName:
        case 'Windows':
            for arch in archs:
                cmd = f'conan create -s os={osName} -s arch={arch} -s compiler="{compiler}" -s compiler.version={compilerVersion} -s compiler.runtime=MD -s build_type=Release {addition_settings}  {conanfile} 1602/{chn}'
                print(cmd)    
                os.system(cmd)
                if debug:
                    cmd=f'conan create -s os={osName} -s arch={arch} -s compiler="{compiler}" -s compiler.version={compilerVersion} -s compiler.runtime=MDd -s build_type=Debug {addition_settings}   {conanfile} 1602/{chn}'
                    print(cmd)    
                    os.system(cmd)
        case _:
            for arch in archs:
                cmd=f'conan create -s os={osName} -s arch={arch} -s compiler="{compiler}" -s compiler.version={compilerVersion} -s build_type=Release {addition_settings}  {conanfile} 1602/{chn}'
                print(cmd)    
                os.system(cmd)
                if debug:
                    cmd=f'conan create -s os={osName} -s arch={arch} -s compiler="{compiler}" -s compiler.version={compilerVersion} -s build_type=Debug {addition_settings}  {conanfile} 1602/{chn}'
                    print(cmd)    
                    os.system(cmd)

def build_android(conanfile:str, chn:str, compiler:str, compilerVersion:str, archs:list, debug:bool, addition_settings:str=''):
    for arch in archs:
        cmd=f'conan create -s os=Android -s arch={arch} -s compiler="{compiler}" -s compiler.version={compilerVersion} -s build_type=Release {addition_settings}  {conanfile} 1602/{chn}'
        print(cmd)    
        os.system(cmd)
        if debug:
            cmd=f'conan create -s os=Android -s arch={arch} -s compiler="{compiler}" -s compiler.version={compilerVersion} -s build_type=Debug {addition_settings}  {conanfile} 1602/{chn}'
            print(cmd)    
            os.system(cmd)
    
def build_ios(conanfile:str, chn:str, compiler:str, compilerVersion:str, archs:list, debug:bool, addition_settings:str=''):
    for arch in archs:
        cmd=f'conan create -s os=iphoneOS -s arch={arch} -s compiler={compiler} -s compiler.version={compilerVersion} -s build_type=Release {addition_settings}  {conanfile} 1602/{chn}'
        print(cmd)    
        os.system(cmd)
        if debug:
            cmd=f'conan create -s os=iphoneOS -s arch={arch} -s compiler={compiler} -s compiler.version={compilerVersion} -s build_type=Debug {addition_settings}  {conanfile} 1602/{chn}'
            print(cmd)    
            os.system(cmd)

def rm_error_handler(func, path, execinfo):
    os.chmod(path, stat.S_IWUSR)
    func(path)

def read_target_name(file:str)->str:
    f = open(file, 'r', encoding='utf-8')
    for line in f.readlines():
        l = line.replace(' ', '')
        l = l.replace('\t', '')
        if l.startswith('name='):
            return l.removeprefix('name=')

    return None

def read_target_version(file:str)->str:
    f = open(file, 'r', encoding='utf-8')
    for line in f.readlines():
        l = line.replace(' ', '')
        l = l.replace('\t', '')
        if l.startswith('version='):
            return l.removeprefix('version=')

    return None

def run():
    parser = argparse.ArgumentParser(
        description='Generate project files of MaxME based platform etc.')

    parser.add_argument("target", help="the target project name.special an predefined project name or an 'conanfile.py.in'")
    parser.add_argument("-t", "--tag", help="the git tag of target, if specified,  use 'stable' conan channel and use 'tag' as version")
    parser.add_argument("-b","--branch", help="the git branch of target, if specified, use 'branch' as conan channel")
    parser.add_argument("-r", "--ref", help="the git ref identify of target, if specified, use 'dev' as conan chanel and use 'ref' as version")
    parser.add_argument('-v','--version', help='the conan package version, if specified will override default.')
    parser.add_argument('--without_native', action='store_true', help='not build native package')
    parser.add_argument('--android', action='store_true', help='build android package.')
    if platform.system() == 'MacOS':
        parser.add_argument('--ios', action='store_true', help='build ios package.')
    parser.add_argument('--arch', choices=['x86','x86_64','armv7','armv8','all', 'default'], default='default', help='target arch')
    parser.add_argument('--debug', action='store_true', help='build debug package.')
    parser.add_argument('--compiler', choices=['gcc','clang','Visual Studio'], help='the compiler')
    parser.add_argument('--compiler_version', help='the version of compiler')
    parser.add_argument('--upload', action='store_true', help='upload pacakge to conan recip', default=False)
    parser.add_argument('-c', '--chn', help='specify conan channel, will override default rule.')
    parser.add_argument('-s', '--settings', help='specify additional conan settings.', default='')
    parser.add_argument('-e', '--env', help='specify addtional envrioment variables.')
    parser.add_argument('--build_version', help='append building number to version, avalible with CI system.')

    args = parser.parse_args()

    if args.target == 'list':
        print('inside pacakges:\n')
        refs = os.listdir(f'{os.path.dirname(__file__)}/targets')
        for ref in refs:
            if ref.endswith('.py.in'):
                print(ref.removesuffix(".py.in"))
        exit(0)

    git_ref = ''
    version = ''
    git_checkout=''
    chn = 'dev'
    compiler = args.compiler
    compiler_version = args.compiler_version
    archs = []
    target = args.target
    
    conan_file = f'{os.path.dirname(__file__)}/conanfile.py'
    if os.path.exists(conan_file) :
        if os.path.isdir(conan_file):
            shutil.rmtree(conan_file)
        else:
            os.remove(Path(conan_file))

    reposes_config = open(f'{os.path.dirname(__file__)}/targets/repos.yaml', "r", encoding='utf-8')
    reposes = yaml.load(reposes_config, Loader=yaml.Loader)

    tmpl_file = args.target
    if not Path(tmpl_file).is_file() :
        if find_target(f'{os.path.dirname(__file__)}/targets', f'{tmpl_file}.py.in'):
            tmpl_file = f'{os.path.dirname(__file__)}/targets/{tmpl_file}.py.in'
        else:
            print('Error: Invalid target.')
            exit(-1)
    else:
        target = read_target_name(tmpl_file)
        version = read_target_version(tmpl_file)

    if (not compiler) or len(compiler) == 0 :
        match platform.system():
            case 'Windows':
                compiler='Visual Studio'
            case 'MacOS':
                compiler='clang'
            case _:
                compiler='gcc'
    if (not compiler_version) or len(compiler_version) == 0 :
        match compiler:
            case 'Visual Studio':
                compiler_version= '15'
            case 'clang':
                compiler_version= '10.1'
            case 'gcc':
                ver = os.popen('gcc -dumpversion')
                compiler_version= ver.read()
    if args.arch == 'all':
        match platform.system():
            case 'Windows':
                archs.append('x86')
                archs.append('x86_64')
            case _:
                archs.append('x86')
                archs.append('x86_64')
                archs.append('armv7')
                archs.append('armv8')
    elif args.arch == 'default':
        match platform.system():
            case 'Windows':
                archs.append('x86')
                archs.append('x86_64')
            case _:
                archs.append('x86_64')
    else:
        archs.append(args.arch)    

    if args.tag :
        git_ref = args.tag.strip()
        version = args.tag.strip()
        chn = 'stable'
    elif args.ref :
        git_ref = args.ref.strip()
        version = args.ref.strip()
        git_checkout = f'self.run("git checkout {args.ref.strip()}")'
    elif args.branch :
        git_ref = args.branch.strip()
        chn = args.branch.strip()
    
    if len(version) == 0:
        repos = reposes[args.target]
        if not repos:
            Warning('not detected version.')
        else:
            os.system(f'git clone {repos} -b {args.branch} src')
            os.chdir('src')
            version = os.popen('git rev-parse --short HEAD').read()
            version = version.replace('\n', '')
            os.chdir('..')
            os.system('rm -fr src')

    if args.version:
        version = args.version
    if args.chn:
        chn = args.chn
    if args.build_version:
        version += f'.{args.build_version}'

    if args.env:
        envs = args.env.split(',')
        for env in envs:
            kv = env.split('=')
            if len(kv) == 2:
                os.putenv(kv[0], kv[1])
        
    shutil.copyfile(tmpl_file, conan_file)
    replace_in_file(conan_file, '@checkout@', git_checkout)
    if len(git_checkout) >0:
        replace_in_file(conan_file, '@git_ref@', '')
    else:
        replace_in_file(conan_file, '@git_ref@', f'-b {git_ref}')
    if len(version) >0 :
        replace_in_file(conan_file, '@version@', version)

    if not args.without_native:
        build_native(conan_file, chn, compiler, compiler_version, archs, args.debug, args.settings)
    if args.android:
        build_android(conan_file, chn, compiler, compiler_version, ['arm','aarch64'], args.debug, args.settings)
    if platform.system() == 'MacOS':
        if args.ios:
            build_ios(conan_file, chn, compiler, compiler_version, ['aarch64'], args.debug, args.settings)

    if args.upload:
        os.system(f'conan upload {target}/{version}@1602/{chn} --all --force')

if __name__ == "__main__":
    sys.exit(run())