# Stackd IAC

IAC stack

## Usage

### initializing project

~~~
$ stackd init
~~~

Add --help for usage message. Initalizes new project in current directory. Clones core specifications,
terraform provider versions, setups vault. 

## Updating binaries and repos

~~~
$ stackd update
~~~

binaries and repos will be synced with stackd.yaml project file

## Building infrastructure code

~~~
$ stackd build
~~~

Builds IAC specifications for all configured clusters

## running terragrunt plan

~~~
$ stackd plan build/<cluster>/<stack>/<module>
~~~

add -b to build before run terragrunt

~~~
$ stackd plan build/<cluster>/<stack>/<module> -b
~~~

## available commands

~~~
$ stackd

Usage: stackd [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  apply
  build
  create
  destroy
  init
  output
  plan
  run-all
  update
~~~
