#!/usr/bin/python

from apache_auditor import ApacheAuditor


def main():

    apache_auditor = ApacheAuditor()
    apache_auditor.audit_apache()

    return 0

if __name__ == '__main__':
    main()
