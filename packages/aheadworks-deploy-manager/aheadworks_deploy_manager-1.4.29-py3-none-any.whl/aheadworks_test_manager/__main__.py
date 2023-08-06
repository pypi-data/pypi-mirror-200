#!/usr/bin/env python3
from aheadworks_core.api.composer_manager import ComposerManager
from aheadworks_core.model.cd import Cd as cd
import subprocess
import click
from os.path import join as _
import os
import re
import json
import pathlib
import time
import shutil

def remove_listeners(path):
    with open(path) as phpunit_config:
        data = phpunit_config.read()
        reg = re.compile("<listeners.*</listeners>", re.S)
        data = re.sub(reg, '', data)
    with open(path, 'w') as phpunit_config:
        phpunit_config.write(data)

def di_compile():
    proc = subprocess.run([_(BASIC_PATH, 'bin/magento'), 'module:enable', '--all'])
    ec3 = proc.returncode
    proc = subprocess.run([_(BASIC_PATH, 'bin/magento'), 'setup:di:compile'])
    ec4 = proc.returncode

    print(ec3)
    print(ec4)

    if ec3 or ec4:
        print("Failed to di:compile")

def install(path):
    """
    Install extension(s) to path from path or zip
    """
    click.echo("Installing from %s" % path)

    with open(_(path, 'composer.json')) as f:
        composer = json.load(f)
        repo_name = re.sub(r'[^a-z0-9_]', '_', composer['name'])

    with cd(BASIC_PATH):
        subprocess.run(['composer', 'config', 'repositories.aheadworks', 'composer', 'https://composer.do.staging-box.net'])
        subprocess.run(['composer', 'config', 'http-basic.repo.magento.com', 'bf08744e4b4b3aee1d54fcd7cd56194a', 'f5b232eab5158a4597ecb00f8cacdf4a'])
        subprocess.run(['composer', 'config', 'repositories.' + repo_name, 'path', path])

        proc = subprocess.Popen(['php', '-d', 'memory_limit=4G', '/usr/local/bin/composer', 'require', '--prefer-dist', '{e[name]}:{e[version]}'.format(e=composer)])
        proc.communicate()

        if proc.returncode:
            raise click.ClickException("Failed to install extension")

    result_path = BASIC_PATH / 'vendor' / composer['name']
    return result_path


@click.group()
def cli():
    click.echo("Removing phpunit listeners")
    remove_listeners(BASIC_PATH / 'dev' / 'tests' / 'unit' / 'phpunit.xml.dist')


@cli.command()
@click.option('--severity', default=9, help='Severity level.')
@click.option('--report', default="junit", help='Report type.', type=click.Choice(["full", "xml", "checkstyle", "csv",
                                                                             "json", "junit", "emacs", "source",
                                                                             "summary", "diff", "svnblame", "gitblame",
                                                                             "hgblame", "notifysend"]))
@click.argument('path', type=click.Path(exists=True))
@click.argument('report_file', type=click.Path(), required=False)
def codesniffer(severity, report, path, report_file):
    """Run codesniffer tests against the path"""

    os.system("mkdir -p test-results")
    if os.getenv('SEVERITY'):
        severity = os.getenv('SEVERITY')

    options = [
        _(BASIC_PATH, 'vendor/bin/phpcs'),
        path
    ]

    options += ['--severity=%s' % severity]
    options += ['--standard=Magento2']
    options += ['--extensions=php,phtml']

    stdout = None
    if report_file:
        options += ['--report=' + report]
        stdout = open(report_file, 'w')

    process = subprocess.run(options, stdout=stdout)
    exit(process.returncode)


@cli.command()
@click.option('--report', default="junit", help='Report type.', type=click.Choice(["junit"]))
@click.argument('path', type=click.Path(exists=True))
@click.argument('report_file', type=click.Path(), required=False)
def unit(report, path, report_file):
    """Run unit tests for extension at path"""

    os.system("mkdir -p test-results")
    install(path)
    di_compile()
    
    try:
        os.mkdir('allure')
        shutil.copyfile("/var/www/html/dev/tests/unit/allure/allure.config.php", "allure/allure.config.php")
    except:
        print('allure config not found, its unit test for 2.4.4')
    
    options = [
        _(BASIC_PATH, 'vendor/bin/phpunit'),
        '--configuration',  _(BASIC_PATH, 'dev/tests/unit/phpunit.xml.dist')
    ]

    if report_file:
        options += ['--log-%s' % report, report_file]

    proc = subprocess.Popen(options + [_(path, 'Test/Unit')])
    proc.communicate()

    if not report_file:
        exit(proc.returncode)

    exit(proc.returncode)


@cli.command()
@click.option('--severity', default=0, help='Severity level.')
@click.option('--report', default="junit", help='Report type.', type=click.Choice(["junit"]))
@click.argument('path', type=click.Path(exists=True))
@click.argument('report_file', type=click.Path(), required=False)
def phpstan(severity, report, path, report_file):
    """Run phpstan static analysis against the path"""

    os.system("mkdir -p test-results")
    install(path)
    di_compile()

    options = [
        _(BASIC_PATH, 'vendor/bin/phpstan'),
        'analyse',
        path
    ]

    config = _(path, 'phpstan.neon')
    if pathlib.Path(config).is_file():
        options += ['--configuration', config]

    if os.getenv('PHPSTANSEVERITY'):
        options += ['--level', os.getenv('PHPSTANSEVERITY')]
    else:
        options += ['--level', str(severity)]

    options += [
        '--autoload-file',
        _(BASIC_PATH, 'dev/tests/integration/framework/autoload.php')
    ]

    stdout = None
    if report_file:
        options += ['--error-format', report]
        stdout = open(report_file, 'w')

    process = subprocess.run(options, stdout=stdout)
    exit(process.returncode)


@cli.command()
@click.option('--report', default='xml', help='Report type.', type=click.Choice(['xml']))
@click.argument('path', type=click.Path(exists=True))
@click.argument('report_file', type=click.Path(), required=False)
def mess_detector(report, path, report_file):
    """Run mess detector against the path"""

    os.system("mkdir -p test-results")
    install(path)

    if not report_file:
        report = 'ansi'

    options = [
        _(BASIC_PATH, 'vendor/bin/phpmd'),
        path,
        report,
        _(BASIC_PATH, 'dev/tests/static/testsuite/Magento/Test/Php/_files/phpmd/ruleset.xml')
    ]

    stdout = None
    if report_file:
        stdout = open(report_file, 'w')

    process = subprocess.run(options, stdout=stdout)
    exit(process.returncode)


@cli.command()
@click.option('--report', default="junit", help='Report type.', type=click.Choice(["junit"]))
@click.argument('path', type=click.Path(exists=True))
@click.argument('report_file', type=click.Path(), required=False)
def install_magento(report, path, report_file):
    """Run install magento with extension at path"""

    os.system("mkdir -p test-results")
    install(path)
    global output

    try:
        output = subprocess.run(
            ['sh', "/tmp/create-install-dump.sh", '--withoutdump'],
            check=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        os.system("mkdir logs1")
        os.system("mysqldump -uroot -proot magento >> logs1/dump.sql")
        os.system(f"cp /var/www/html/var/log/* logs1")
        os.system("cp /var/www/html/app/etc/* logs1")
        exit(e.returncode)

    exit(output.returncode)

@cli.command()
@click.argument('path', type=click.Path(exists=True))
def validate_m2_package(path):
    """
    Test marketplace package
    :param path:
    :return:
    """
    #proc = subprocess.Popen(['php', '-f', '/usr/local/bin/validate_m2_package.php', path])
    #proc.communicate()
    #exit(proc.returncode)


if __name__ == '__main__':
    BASIC_PATH = pathlib.Path(os.environ.get('MAGENTO_ROOT', '/var/www/html'))
    ComposerManager.init_extra_repos()
    cli()
