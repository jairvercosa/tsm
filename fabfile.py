# -*- coding: ISO-8859-1 -*-
from fabric.api import *
#Default release - 0.0.1

env.release = '0.0.1'

def production():
    """Confgs da producao"""
    env.settings = 'production'
    env.user = 'root'
    env.password = 'totvs@123'
    env.path = '/tsmproducao'
    env.hosts = ['10.10.2.132']
    env.port = 22

def testenv():
    """Confgs para teste"""
    env.settings = 'testenv'
    env.user = 'root'
    env.password = 'totvs@123'
    env.path = '/tsmteste'
    env.hosts = ['10.10.2.132']
    env.port = 22

def setup():
    """Setup virtual env"""
    #run('mkdir -p %(path)s; cd %(path)s; virtualenv --no-site-packages .; mkdir -p releases; mkdir -p shared;' % env)
    clone_repo()
    checkout_latest()
    #install_requirements()

def deploy():
    """Deploy da ultima versao"""
    checkout_latest()
    #install_requirements()
    symlink_current_release()
    migrate()
    restart_server()

def clone_repo():
    """Realiza o clone do repositorio"""
    run('cd %(path)s; rm -rf %(path)s/repository' % env)
    run('cd %(path)s; git clone https://jairvercosa@bitbucket.org/jairvercosa/totvs-sales-management.git repository' % env)

def checkout_latest():
    """Atualiza ultimo codigo no repositorio"""
    import time
    env.release = time.strftime('%Y%m%d%H%M%S')
    if env.settings=='testenv':
        run("cd %(path)s/repository; git pull origin master" % env)
    else:
        run("cd %(path)s/repository; git pull origin master" % env)

    run("cp -R %(path)s/repository %(path)s/releases/%(release)s; rm -rf %(path)s/releases/%(release)s/.git*" % env)

def install_requirements():
    """instala requisitos do sistema"""
    run('cd %(path)s; %(path)s/bin/pip install -r ./releases/%(release)s/requirements.txt' % env)

def symlink_current_release():
    """carrega arquivos de setting"""
    with settings(warn_only=True):
        run('cd %(path)s; rm releases/previous; mv releases/current releases/previous;' % env)

    # link para pasta current para a release atual
    run('cd %(path)s; ln -s %(release)s releases/current' % env)
    
    # copia para as pastas que são usadas no webserver
    run('cd %(path)s; cp -r releases/current/* tsm;' % env) #tsm padrão
    run('cd %(path)s; cp -r releases/current/* %(path)s_fluig/tsm;' % env) #tsm fluig
    
    # acerta arquivo de setting
    run('cd %(path)s/releases/current/tsm/; mv settings_%(settings)s.py %(path)s/tsm/tsm/settings.py' % env) #tsm padrão
    run('cd %(path)s/releases/current/tsm/; mv settings_%(settings)s_fluig.py %(path)s_fluig/tsm/tsm/settings.py' % env) #tsm fluig

    run('%(path)s/bin/python %(path)s/tsm/manage.py collectstatic' % env)

    with settings(warn_only=True):
        run('rm %(path)s/shared/static' % env)
        run('cd %(path)s/releases/current/tsm/core/static/; ln -s %(path)s/releases/%(release)s/tsm/core/static %(path)s/shared/static' % env)

def migrate():
    """Executa migrates do sistema"""
    # tsm padrão
    print "Migrate of tsm padrao..........."
    run('cd %(path)s/releases/current; ../../bin/python %(path)s/tsm/manage.py migrate tsm.acesso' % env)
    run('cd %(path)s/releases/current; ../../bin/python %(path)s/tsm/manage.py migrate tsm.cliente' % env)
    run('cd %(path)s/releases/current; ../../bin/python %(path)s/tsm/manage.py migrate tsm.core' % env)
    run('cd %(path)s/releases/current; ../../bin/python %(path)s/tsm/manage.py migrate tsm.equipe' % env)
    run('cd %(path)s/releases/current; ../../bin/python %(path)s/tsm/manage.py migrate tsm.oportunidade' % env)

    # tsm fluig
    print "Migrate of tsm fluig............"
    run('cd %(path)s/releases/current; ../../bin/python %(path)s_fluig/tsm/manage.py migrate tsm.acesso' % env)
    run('cd %(path)s/releases/current; ../../bin/python %(path)s_fluig/tsm/manage.py migrate tsm.cliente' % env)
    run('cd %(path)s/releases/current; ../../bin/python %(path)s_fluig/tsm/manage.py migrate tsm.core' % env)
    run('cd %(path)s/releases/current; ../../bin/python %(path)s_fluig/tsm/manage.py migrate tsm.equipe' % env)
    run('cd %(path)s/releases/current; ../../bin/python %(path)s_fluig/tsm/manage.py migrate tsm.oportunidade' % env)

def rollback():
    run('cd %(path)s; mv releases/current releases/_previous;' % env)
    run('cd %(path)s; mv releases/previous releases/current;' % env)
    run('cd %(path)s; mv releases/_previous releases/previous;' % env)
    restart_server()

def restart_server():
    """Reinicia servicos"""
    if env.settings!='testenv':
        with settings(warn_only=True):
            run('/etc/init.d/nginx stop')
            # tsm padrão
            run('kill -8 `cat %(path)s/uwsgi_pid.pid`' % env)
            run('rm -f %(path)s/tsm.sock' % env)
            # tsm fluig
            run('rm -f %(path)s_fluig/tsm.sock' % env)
            run('kill -8 `cat %(path)s_fluig/uwsgi_pid.pid`' % env)
        
        run('uwsgi --ini %(path)s/uwsgi.ini' % env) # tsm padrão
        run('uwsgi --ini %(path)s_fluig/uwsgi.ini' % env) # tsm fluig
    run('/etc/init.d/nginx start')