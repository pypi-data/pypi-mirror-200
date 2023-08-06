from setuptools import setup, find_packages

setup(
    name='devops-auto-tools',
    version='1.1.3',    
    description='A Python project for eks, ssh, jumpm-proxy manager',
    author='Baristi Trieu',
    author_email='ltqtrieu.0204@gmail.com',
    packages=find_packages(),
    license ='MIT',
    install_requires=[
        'simple_term_menu==1.4.1',
        'sshuttle==1.1.1'
    ],
    
    entry_points={
        'console_scripts': [
            'eksm  = tools.main:eksm' ,
            'sshm  = tools.main:sshm' ,
            'jumpm = tools.main:jumpm'
        ]
    },
    
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.8',
    ],
)
