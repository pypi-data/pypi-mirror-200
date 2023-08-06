========
Usage
========

*pcrunner* can run as a daemon on Linux, as a service on win32 and has a
command.

*pcrunner*'s has sensible defaults which can be overridden by the configuration
file. Most of the options in the configuration file can be overriden by command
line options.

pcrunner command line arguments and options::

    $ pcrunner --help
    usage: pcrunner [-h] [-c CONFIG_FILE] [-n NSCA_WEB_URL] [-u NSCA_WEB_USERNAME]
                    [-p NSCA_WEB_PASSWORD] [-o COMMAND_FILE] [-H HOSTNAME]
                    [-i INTERVAL] [-m MAX_PROCS] [-e LINES_PER_POST]
                    [-r RESULT_FILE] [-d RESULT_DIR] [-f PID_FILE]
                    [-t HTTP_TIMEOUT] [-s MAX_LINE_SIZE] [-l LOG_FILE] [-a] [-v]
                    [--version]
                    [{start,stop}]

    Passive Command Runner.

    positional arguments:
      {start,stop}          Start or stop pcrunner runloop

    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG_FILE, --config-file CONFIG_FILE
                            Configuration file
      -n NSCA_WEB_URL, --nsca_web_url NSCA_WEB_URL
                            NSCA server url.
      -u NSCA_WEB_USERNAME, --nsca-web-username NSCA_WEB_USERNAME
                            NSCA Web username.
      -p NSCA_WEB_PASSWORD, --nsca-web-password NSCA_WEB_PASSWORD
                            NSCA Web password.
      -o COMMAND_FILE, --command-file COMMAND_FILE
                            Command file.
      -H HOSTNAME, --hostname HOSTNAME
                            Hostname excpected by Nagios/Icinga.
      -i INTERVAL, --interval INTERVAL
                            Time interval between checks in seconds.
      -m MAX_PROCS, --max-procs MAX_PROCS
                            Max processes to run simultaneously.
      -e LINES_PER_POST, --lines-per-post LINES_PER_POST
                            number of lines per HTTP post
      -r RESULT_FILE, --result-file RESULT_FILE
                            File to where results are written to when NSCA
                            webserver is not reachable.
      -d RESULT_DIR, --result-dir RESULT_DIR
                            Directory for results from external commands.
      -f PID_FILE, --pid-file PID_FILE
                            PID file
      -t HTTP_TIMEOUT, --http-timeout HTTP_TIMEOUT
                            Max secs to timeout when posting results to NSCA
                            webserver
      -s MAX_LINE_SIZE, --max-line-size MAX_LINE_SIZE
                            Maximum result data to post to NSCA webserver in bytes
                            per line.
      -l LOG_FILE, --log-file LOG_FILE
                            log file
      -a, --no-daemon       Run pcrunner in foreground
      -v, --verbose         Show verbose info (level DEBUG).
      --version             Show version


example config:

.. code-block:: yaml

  ---
  # NSCW Web url
  # Default: http://localhost:5668/queue
  nsca_web_url: http://localhost:5668/queue

  # NSCW Web username
  # Default: default
  nsca_web_username: default

  # NSCW Web password
  # Default: changeme
  nsca_web_password: changeme

  # hostname of local host (host that is being checked)
  # Default: <gethostname>
  hostname: host.example.com

  # pid file
  # Default: /var/run/pcrunner.pid as root
  # or <OS tempdir>/pcrunner.pid'
  pid_file: /var/run/pcrunner.pid

  # log file, when configured don't use syslog
  # Default: null
  log_file: null

  # Verbose logging
  # Default: False
  verbose: False

  # File with check commands
  # Default win32: <python_site-packages_dir>/pcrunner/etc/commands.yml
  # Default POSIX: /etc/pcrunner/commands.yml
  command_file: /etc/pcrunner/commands.yml

  # Directory for results from external commands
  # Must be writable for external commands and pcrunner
  # Example: /var/spool/pcrunner/results
  # Default: null
  result_dir: /var/spool/pcrunner/results

  # Temp file for results not yet uploaded to NSCA Web
  # Default win32: <python_site-packages_dir>/pcrunner/data/pcrunner.dat
  # Default POSIX: /var/spool/pcrunner/pcrunner.dat
  result_file: /var/spool/pcrunner/pcrunner.dat

  # Number of maximum process to run concurrent
  # Default: CPU count
  max_procs: 2

  # Time interval between checks in seconds
  # Default: 60
  interval: 60

  # Max secs to timeout when posting results to NSCA webserver
  # Default: 3
  http_timeout: 3

  # FQDN Syslog server
  # Default: null
  syslog_server: null

  # Syslog server port
  # Default: 514
  syslog_port: 514

  # Number of lines per HTTP post
  # Default: 400
  lines_per_post: 400

  # Maximum result data to post to NSCA webserver in bytes per line.
  # Default: 8192 bytes (max length of an external command)
  max_line_size: 8192
