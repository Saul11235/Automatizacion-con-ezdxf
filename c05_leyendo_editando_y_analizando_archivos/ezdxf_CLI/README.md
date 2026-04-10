usage: ezdxf [-h] [-V] [-f] [-v] [--config CONFIG] [--log LOG]
             {audit,draw,view,browse,browse-acis,strip,config,info,hpgl} .
..

Command launcher for the Python package "ezdxf":
https://pypi.org/project/ezdxf/

positional arguments:
  {audit,draw,view,browse,browse-acis,strip,config,info,hpgl}
#    audit               audit and repair DXF files
#    draw                draw and save DXF as a bitmap or vector image
#    view                view DXF files by the PyQt viewer
#    browse              browse DXF file structure
#    browse-acis         browse ACIS structures in DXF files
    strip               strip comments from DXF files
    config              manage config files
    info                show information and optional stats of DXF files
                        as loaded by ezdxf, this may not represent the
                        original content of the file, use the browse
                        command to see the original content
    hpgl                view and/or convert HPGL/2 plot files to various
                        formats

options:
#  -h, --help            show this help message and exit
  -V, --version         show version and exit
  -f, --fonts           rebuild system font cache and print all fonts
                        found
  -v, --verbose         give more output
  --config CONFIG       path to a config file
  --log LOG             path to a verbose appending log, "stderr" logs
                        to the standard error stream
:
