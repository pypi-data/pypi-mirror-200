'''
Created on 2023-04-01

@author: wf
'''
from argparse import ArgumentParser #Namespace
from argparse import RawDescriptionHelpFormatter
from profiwiki.version import Version
from profiwiki.profiwiki_core import ProfiWiki
#from pathlib import Path
import sys
import traceback
import webbrowser


class ProfiWikiCmd():
    """
    ProfiWiki command line
    """
    
    def get_arg_parser(self, description: str, version_msg) -> ArgumentParser:
        """
        Setup command line argument parser
        
        Args:
            description(str): the description
            version_msg(str): the version message
            
        Returns:
            ArgumentParser: the argument parser
        """
        #script_path=Path(__file__)
        parser = ArgumentParser(description=description, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-a", "--about", help="show about info [default: %(default)s]", action="store_true")
        parser.add_argument("-c", "--create",action="store_true",help="create the wiki")  
        parser.add_argument("--cron",action="store_true",help="start cron service")  
        parser.add_argument("-d", "--debug", dest="debug",   action="store_true", help="set debug [default: %(default)s]")
        parser.add_argument("-fa", "--fontawesome",   action="store_true", help="install fontawesome")
        parser.add_argument("-fr", "--forcerebuild",   action="store_true", help="force the rebuild")
        parser.add_argument("-kr", "--killremove",action="store_true", help="kill and remove my containers")
        parser.add_argument("-pu", "--plantuml",   action="store_true", help="install plantuml")
        parser.add_argument("--port", type=int, default=9042, help="the port to serve from [default: %(default)s]")
        parser.add_argument("--prefix",default="pw",help="the container name prefix to use [default: %(default)s]")
        parser.add_argument('-q', '--quiet', help="not verbose [default: %(default)s]",action="store_true")
        parser.add_argument("-i", "--info", help="show system info", action="store_true")
        parser.add_argument("-V", "--version", action='version', version=version_msg)
        return parser
    
def main(argv=None):  # IGNORE:C0111
    """main program."""

    if argv is None:
        argv = sys.argv[1:]

    program_name = "profiwiki"
    program_version = f"v{Version.version}"
    program_build_date = str(Version.date)
    program_version_message = f'{program_name} ({program_version},{program_build_date})'

    args = None
    try:
        pw_cmd = ProfiWikiCmd()
        parser = pw_cmd.get_arg_parser(description=Version.license, version_msg=program_version_message)
        args = parser.parse_args(argv)
        if len(argv) < 1:
            parser.print_usage()
            sys.exit(1)
        if args.about:
            print(program_version_message)
            print(f"see {Version.doc_url}")
            webbrowser.open(Version.doc_url)
        pw=ProfiWiki(args) 
        if args.info:
            info=pw.system_info()
            print(info)
        pw.work()

    except KeyboardInterrupt:
        ###
        # handle keyboard interrupt
        # ###
        return 1
    except Exception as e:
        if DEBUG:
            raise e
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        if args is None:
            print("args could not be parsed")
        elif args.debug:
            print(traceback.format_exc())
        return 2

DEBUG = 1
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-d")
    sys.exit(main())