from KalturaClient import *
from KalturaClient.Plugins.Core import *
import configparser
import csv
import sys
import csv
import datetime

my = {}


def initBase(cfgFilename, outName):
    global my
    my['map'] = {}
    kini = configparser.ConfigParser()
    kini.read(cfgFilename,encoding='utf-8-sig')
    my['partnerId'] = kini['KALTURA']['PARTNER_ID']
    my['adminSecret'] = kini['KALTURA']['ADMIN_SECRET']
    my['userId'] = kini['KALTURA']['USER_ID']
    my['csvfile'] = open(outName, 'w', newline='')
    my['spamwriter'] = csv.writer(my['csvfile'])
    my['spamwriter'].writerow(['Institution ID', 'User ID', 'Course Title', 'Course Identifier', 'Course Group Name', 'Associated with Course in HLC', 'Score', 'Complete Date',
                               'Accrediting Body Name', 'Course Provider Name', 'Accredited Provider Init Date', 'Accredited Provider Expiration Date', 'Credits', 'Estimated Completion Time'])


def initKaltura():
    global my
    my['config'] = KalturaConfiguration(my['partnerId'])
    my['config'].serviceUrl = 'https://www.kaltura.com/'
    my['client'] = KalturaClient(my['config'])
    my['ks'] = my['client'].session.start(
        my['adminSecret'], my['userId'], KalturaSessionType.ADMIN, my['partnerId'])
    my['client'].setKs(my['ks'])


def topContentForDate(forDate):
    global my
    my['forDate'] = forDate
    print(forDate)
    report_type = KalturaReportType.TOP_CONTENT
    report_input_filter = KalturaReportInputFilter()
    report_input_filter.fromDay = forDate
    report_input_filter.toDay = forDate
    pager = KalturaFilterPager()
    pager.pageIndex = 1
    pager.pageSize = 99
    order = ''
    object_ids = ''
    response_options = KalturaReportResponseOptions()
    my['result'] = my['client'].report.getTable(
        report_type, report_input_filter, pager, order, object_ids, response_options)


def extractTopEntries():
    global my
    try:
        data = my['result'].getData()
        lines = data.split(';')
        del lines[-1]
        my['entryIds'] = []
        my['entryNames'] = []
        for line in lines:
            tokens = line.split(',')
            my['entryIds'].append(tokens[0])
            my['map'][tokens[0]] = tokens[1]
    except Exception as e:
        print('\n*** EXCEPTION in extractTopEntries {}\n'.format(e))


def usersForEntry(entryId):
    global my
    print('\t', entryId)
    report_type = KalturaReportType.USER_ENGAGEMENT
    report_input_filter = KalturaReportInputFilter()
    report_input_filter.fromDay = my['forDate']
    report_input_filter.toDay = my['forDate']
    pager = KalturaFilterPager()
    pager.pageIndex = 1
    pager.pageSize = 99
    order = ''
    object_ids = entryId
    response_options = KalturaReportResponseOptions()

    result = my['client'].report.getTable(
        report_type, report_input_filter, pager, order, object_ids, response_options)
    data = result.getData()
    users = data.split(';')
    del users[-1]
    for userLine in users:
        user = userLine.split(',')[0]
        if user.lower() != 'unknown':
            my['spamwriter'].writerow(['HCA', user, my['map'][entryId], entryId,
                                       ' ', 0, 100, my['forDate'], ' ', ' ', ' ', ' ', ' ', ' '])
            print('\t\t', user)


def createReport():
    global my
    for entryId in my['entryIds']:
        usersForEntry(entryId)


initBase(sys.argv[1],sys.argv[2])
initKaltura()
curDate = datetime.date.today()
oneDay = datetime.timedelta(days=1)
for _ in range(2):
    topContentForDate(curDate.strftime('%Y%m%d'))
    extractTopEntries()
    createReport()
    curDate -= oneDay
print('\nmy={}'.format(my))
