## Usage example

```
python main.py --input input\keller4.mtx --output keller4.csv ref --agents 100
```

## Command line interface
Common arguments:
```shell
$ python main.py --help

usage: main.py [-h] [--input INPUT] [--output OUTPUT]
               {aco,ref} ...

positional arguments:
  {aco,ref}

optional arguments:
  -h, --help       show this help message and exit
  --input INPUT
  --output OUTPUT
```
Reference algorithm:
```shell
$ python main.py ref --help

usage: main.py ref [-h] [--agents AGENTS]

optional arguments:
  -h, --help       show this help message and exit
  --agents AGENTS  Agents count
```

Ant colony optimizer:
```shell
$ python main.py aco --help

usage: main.py aco [-h] [--iterations ITERATIONS] [--ants ANTS] [--alpha ALPHA]
                   [--rho RHO]

optional arguments:
  -h, --help            show this help message and exit
  --iterations ITERATIONS
                        Number of algorithm iterations
  --ants ANTS           Ants count
  --alpha ALPHA         Alpha parameter
  --rho RHO             Rho parameter
```