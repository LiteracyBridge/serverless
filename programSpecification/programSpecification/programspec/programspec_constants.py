
# This is a bit ugly, but gives a single place to get the spelling right.
from programspec.utils import JsObject

GENERAL = 'General'
CONTENT = 'Content'
DEPLOYMENTS = 'Deployments'
COMPONENTS = 'Components'

PARTNER = 'Partner'
PROGRAM = 'Program'
NUM_DEPLOYMENTS = 'Number of Deployments'
TOP = 'Top'
SUB1 = 'Sub-1'
SUB2 = 'Sub-2'
DEPLOYMENT_NO = 'Deployment #'
PLAYLIST_TITLE = 'Playlist Title'
MESSAGE_TITLE = 'Message Title'
KEY_POINTS = 'Key Points'
SDG_GOALS = 'SDG Goals'
SDG_TARGETS = 'SDG Targets'
DEFAULT_CATEGORY = 'Default Category'
START_DATE = 'Start Date'
END_DATE = 'End Date'
COMPONENT = 'Component'
AFFILIATE = 'Affiliate'
COUNTRY = 'Country'
REGION = 'Region'
DISTRICT = 'District'
COMMUNITY = 'Community'
GROUP_NAME = 'Group Name'
AGENT = 'Agent'
POPULATION = 'Population'
NUM_HOUSEHOLDS = '# HH'
NUM_TBS = '# TBs'
SUPPORT_ENTITY = 'Support Entity'
TAG = 'Tag'
MODEL = 'Model'

LANGUAGE = 'Language'
RECIPIENTID = 'RecipientID'
TALKINGBOOKID = 'TalkingBookId'
DIRECTORY_NAME = 'Directory Name'

required_sheets = [GENERAL, CONTENT, DEPLOYMENTS, COMPONENTS]
# The sheets must have these columns. If there's no 'required_data', they must not be empty.
required_columns = {
    GENERAL: [PARTNER, PROGRAM, NUM_DEPLOYMENTS],
    CONTENT: [DEPLOYMENT_NO, PLAYLIST_TITLE, MESSAGE_TITLE, KEY_POINTS, SDG_GOALS, SDG_TARGETS, DEFAULT_CATEGORY],
    DEPLOYMENTS: [DEPLOYMENT_NO, START_DATE, END_DATE],
    COMPONENTS: [COMPONENT],
    'recipient': [AFFILIATE, PARTNER, COMPONENT, COUNTRY, REGION, DISTRICT, COMMUNITY, GROUP_NAME, AGENT,
                  POPULATION, NUM_HOUSEHOLDS, NUM_TBS, SUPPORT_ENTITY, MODEL, LANGUAGE]
}
# Only these columns in the given sheet is *required* to have data. The column is still required, but can be blank.
required_data = {
    CONTENT: [DEPLOYMENT_NO, PLAYLIST_TITLE, MESSAGE_TITLE, KEY_POINTS],
    DEPLOYMENTS: [DEPLOYMENT_NO, START_DATE, END_DATE],
    'recipient': [AFFILIATE, PARTNER, COMPONENT, COUNTRY, COMMUNITY, NUM_TBS, SUPPORT_ENTITY, MODEL, LANGUAGE]
}
optional_columns = {
    GENERAL: [TOP, SUB1, SUB2],
    CONTENT: [LANGUAGE, TAG], # [COMPONENT, COUNTRY, REGION, DISTRICT, COMMUNITY, GROUP_NAME, MODEL, LANGUAGE],
    DEPLOYMENTS: [COMPONENT, COUNTRY, REGION, DISTRICT, COMMUNITY, GROUP_NAME, MODEL, LANGUAGE, TAG],
    'recipient': [RECIPIENTID, DIRECTORY_NAME, TAG, TALKINGBOOKID]
}
# These columns are coerced to str() when loaded from the spreadsheet.
string_columns = {
    GENERAL: [PARTNER, PROGRAM],
    CONTENT: [PLAYLIST_TITLE, MESSAGE_TITLE, KEY_POINTS, DEFAULT_CATEGORY, LANGUAGE, TAG],
    DEPLOYMENTS: [COMPONENT, COUNTRY, REGION, DISTRICT, COMMUNITY, GROUP_NAME, MODEL, LANGUAGE, TAG],
    COMPONENTS: [COMPONENT],
    'recipient': [AFFILIATE, PARTNER, COMPONENT, COUNTRY, REGION, DISTRICT, COMMUNITY, GROUP_NAME, AGENT,
                   SUPPORT_ENTITY, MODEL, LANGUAGE, RECIPIENTID, DIRECTORY_NAME, TAG, TALKINGBOOKID]
}

# build a map between the spreadsheet column names and valid member names, 'Group Name' -> 'group_name', '# TBs' -> 'num_tbs'

def column_names_to_member_names(column_names):
    result = {}
    for column_name in column_names:
        member_name = column_name.replace(' ', '_').replace('#', 'num').lower()
        result[column_name] = member_name
    return result

def columns_to_members_map(*sheet_names):
    result = {}
    for sheet_name in sheet_names:
        if sheet_name in required_columns:
            result.update(column_names_to_member_names(required_columns[sheet_name]))
            # for column_name in required_columns[sheet_name]:
            #     tuple_name = column_name.replace(' ', '_').replace('#', 'num').lower()
            #     result[column_name] = tuple_name
        if sheet_name in optional_columns:
            result.update(column_names_to_member_names(optional_columns[sheet_name]))
            # for column_name in optional_columns[sheet_name]:
            #     tuple_name = column_name.replace(' ', '_').replace('#', 'num').lower()
            #     result[column_name] = tuple_name
    return result

# If a column name changes, above, change it here, AND CHANGE USES IN THE CODE!
def check_names():
    manual_prop_map = {
        'Partner': 'partner',
        'Program': 'program',
        'Number of Deployments': 'number_of_deployments',
        'Top': 'top',
        'Sub-1': 'sub-1',
        'Sub-2': 'sub-2',
        'Deployment #': 'deployment_num',
        'Playlist Title': 'playlist_title',
        'Message Title': 'message_title',
        'Key Points': 'key_points',
        'SDG Goals': 'sdg_goals',
        'SDG Targets': 'sdg_targets',
        'Default Category': 'default_category',
        'Start Date': 'start_date',
        'End Date': 'end_date',
        'Component': 'component',
        'Affiliate': 'affiliate',
        'Country': 'country',
        'Region': 'region',
        'District': 'district',
        'Community': 'community',
        'Group Name': 'group_name',
        'Agent': 'agent',
        'Population': 'population',
        '# HH': 'num_hh',
        '# TBs': 'num_tbs',
        'Support Entity': 'support_entity',
        'Tag': 'tag',
        'Model': 'model',

        'Language': 'language',
        'RecipientID': 'recipientid',
        'Directory Name': 'directory_name',
        'TalkingBookId' : 'talkingbookid'
    }
    auto_prop_map = columns_to_members_map(GENERAL, CONTENT, DEPLOYMENTS, COMPONENTS, 'recipient')
    ok = True
    for column, member in manual_prop_map.items():
        if column not in auto_prop_map:
            print('Column "{}" is not found in intrinsic columns'.format(column))
            ok = False
        elif auto_prop_map[column] != member:
            print('Column "{}" expected to be member "{}", found "{}"'.format(column, member, auto_prop_map[column]))
            ok = False
    for column in auto_prop_map.keys():
        if column not in manual_prop_map:
            print('Column "{}" not found manual columns'.format(column))
            ok = False
    if not ok:
        print('Aborting')
        exit(1)

# Check names, then clean up
check_names()
del check_names

# Things that the reconciller can update

DIRECTORIES = 'directories'
XDIRECTORIES = 'xdirectories'
XLSX = 'xlsx'
RECIPIENTS = 'recipientids'
UPDATABLES = JsObject({'words': [DIRECTORIES, XLSX, RECIPIENTS, XDIRECTORIES], 'synonyms': {'dirs': DIRECTORIES, 'xdirs': XDIRECTORIES}})