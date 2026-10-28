import argparse
import requests
from datetime import datetime, timezone

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:158.0) Gecko/20100101 Firefox/158.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/json',
    'Authorization': 'Anonymous',
    'Origin': 'https://timetables.tudublin.ie',
    'Connection': 'keep-alive',
    'Referer': 'https://timetables.tudublin.ie/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
}

json_data = {
    'ViewOptions': {
        'Days': [
            {
                'Name': 'Monday',
                'DayOfWeek': 1,
                'IsDefault': True,
            },
            {
                'Name': 'Tuesday',
                'DayOfWeek': 2,
                'IsDefault': True,
            },
            {
                'Name': 'Wednesday',
                'DayOfWeek': 3,
                'IsDefault': True,
            },
            {
                'Name': 'Thursday',
                'DayOfWeek': 4,
                'IsDefault': True,
            },
            {
                'Name': 'Friday',
                'DayOfWeek': 5,
                'IsDefault': True,
            },
            {
                'Name': 'Saturday',
                'DayOfWeek': 6,
                'IsDefault': True,
            },
        ],
        'Weeks': [],
        'TimePeriods': [
            {
                'Description': 'All Day',
                'StartTime': '00:00',
                'EndTime': '23:59',
                'IsDefault': True,
            },
        ],
        'DatePeriods': [
            {
                'Description': '23/24 All Year',
                'StartDateTime': '2023-08-28T00:00:00+00:00',
                'EndDateTime': '2024-09-01T00:00:00+00:00',
                'IsDefault': True,
                'Type': None,
                'Weeks': [],
            },
        ],
    },
    'CategoryTypesWithIdentities': [
        {
            'CategoryTypeIdentity': '1e042cb1-547d-41d4-ae93-a1f2c3d34538',
            'CategoryIdentities': [
                '6f5b1e73-04d5-d6d0-49f1-6a15a218056e',
            ],
        },
    ],
    'FetchBookings': False,
    'FetchPersonalEvents': False,
    'PersonalIdentities': [],
}

EVENTS_URL = (
    'https://scientia-eu-v4-api-d4-01.azurewebsites.net/api/Public/'
    'CategoryTypes/Categories/Events/Filter/'
    '50a55ae1-1c87-4dea-bb73-c9e67941e1fd'
)
LOCATION_CATEGORY_TYPE = '1e042cb1-547d-41d4-ae93-a1f2c3d34538'
MAX_ROOM_IDS_PER_REQUEST = 15
DEFAULT_ROOM_IDS = [
    '6f5b1e73-04d5-d6d0-49f1-6a15a218056e',
    'b7141bb1-34ef-c64c-4c56-85f67c54e99f',
    '5f509408-5872-bc94-565b-4d90acc9e88d',
    '09b4ae7d-fddd-bd91-1579-38f037463a76',
    'a543f68f-3f70-8263-447c-aefe112f5914',
    '35b277cb-a1ec-b551-fd58-26736e5e5a14',
    'ed96b993-46f8-ef42-f0c8-72fff7922039',
    '64c07835-6a3c-1cb2-e247-5d9ea0ddc3f3',
    '9829cc44-d7d2-e145-e1cc-08ddda4cbc28',
    '88bd148f-e22d-e9c2-c7b3-a22841b4cff9',
    '1a75a569-cffb-0178-fa10-d17bda79d34e',
    '68fcd15c-aafc-f5c4-bae7-92fb58063af4',
    'b9e18a7a-1e7a-6d4e-166f-3083dc65e265',
    '1a700513-4cc9-1587-743e-e2eb98c1573e',
    '19c27753-8198-8bd8-6dc2-ebfecae1af93',
    'a7b52055-3d3f-a0b0-8479-0f352e7a8900',
    '8aac8f2b-e248-8268-d810-5e80cb9a2ad2',
    '8c9bbe49-3430-ce2d-322b-bd0d07e8b8df',
    '76926e85-1786-b70c-2d7c-974afff919f1',
    'e778ab54-4191-1929-3315-524b2ab53020',
    '0198ea16-064f-d7bf-507c-c343a2f67e54',
    'd6d6ad6f-f7d5-482f-d601-48df2dfb17a6',
    'ef463b86-33e4-f200-c4d0-d70c4d7a5414',
    '97a2ce81-7059-7945-245a-ea5a3e8b6f5d',
    '97065a69-a404-e179-be83-4cdc94bf4d20',
    'c372b890-1dba-99c0-f8fc-62250a045dd3',
    '6f53b6e3-84a0-e386-6747-74a3e6eb5443',
    'e5fc491c-87d0-f8da-81cb-3db643c1053f',
    'd6307a8d-1812-63dc-7ebc-640a415bc11d',
    '8e6a8b0d-5b76-af11-8606-8a487a14b3c8',
    'fa04bf40-00fd-bba3-6cc9-a6238368b33e',
    '9f7dc30f-3062-7757-24dd-6f9982e2b81e',
    '0e7fbd65-4164-c73f-d9e0-904272b957cb',
    'a69bc604-4bb5-1430-895f-3c0a9d567d2b',
    '5529f6e2-26b4-9853-718e-0a75bf9599ed',
    '26e72d29-e7d3-3eac-9e52-608355a98eb2',
    '28645d47-21cf-9174-d57d-a4e5c4594728',
    'f215972e-c146-119d-d030-38376eaa7985',
    'cdeb702c-4b03-cafd-a9ca-6b0e5e214f3f',
    '62c97bd2-6baa-45a1-fa4e-017a7bf393f6',
    '95164e5e-f436-24f4-5599-e467e74b172a',
    '6b9141f9-6afb-e949-2587-7d2bc6bf3a69',
    '4a0340f0-69a8-35a0-7f71-f2ce0a0921c4',
    '9aeca4be-651c-f5f3-e6f8-01b0a3f2fc4a',
    '1fbcfdd2-7e2b-68e5-a0bf-831a357a18f5',
    '04a5714a-7dc6-1c12-0c51-5dc81496f3d7',
    'b7dd0a78-7a37-3795-782c-06c1d83a5bde',
    '04006dbb-eb1e-ec7e-6d5f-36586d06a8fe',
    '85f88eeb-6e11-9716-e6c0-0cff5ffc8523',
    'af31e8e9-a649-a36c-091f-e5e9e9b84cf3',
    '959b5148-3b5b-6d82-d945-406d1456e47c',
    '078e9cad-25a0-25f8-818f-0830b5ff4e34',
    '46b82a6a-c14f-e619-d1c1-2650ec7f5149',
    '1ff19b69-8451-cf3f-64e4-bc9181830871',
    '42cb7a67-0066-9000-31ae-2c549451416c',
    '7deee6a6-04b6-d44a-dde0-4fabdfb47e6c',
    'e7785fe5-bbc6-2271-6f84-3bab20d67910',
    '0c5b3aee-1a6f-ac93-377f-15ca8f8df20a',
    'b0b740d6-2445-1ae5-49b8-e9103d59172b',
    '676ec56b-65ea-821c-dd3e-ab47f4c799ad',
    '8997fda7-280b-e0ec-5fc5-7ba617061d18',
    '61923a2b-9b2b-4559-e290-685989bd43ee',
    '3e9d1da9-0472-3b4a-4232-a68c92372fbe',
    '35c7cd8d-18db-7b7c-b362-62402dc2c787',
    '2bfbadcf-9578-9836-016e-0cf2274df5dd',
    'ec59ac5d-5996-c729-e4ce-99d7ff30fda7',
    'b3fabda9-5f6f-9083-4e83-7fc65a819f0b',
    'd50b00b9-71fd-cdde-16dc-08df0e947e45',
    '9b23e40c-c8cc-9103-3824-403d55143354',
]


def _as_utc(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def get_events(start, end, room_ids):
    events = []
    for offset in range(0, len(room_ids), MAX_ROOM_IDS_PER_REQUEST):
        room_batch = room_ids[offset:offset + MAX_ROOM_IDS_PER_REQUEST]
        payload = {
            **json_data,
            'CategoryTypesWithIdentities': [{
                'CategoryTypeIdentity': LOCATION_CATEGORY_TYPE,
                'CategoryIdentities': room_batch,
            }],
        }
        response = requests.post(
            EVENTS_URL,
            params={
                'startRange': start.astimezone(timezone.utc).isoformat(),
                'endRange': end.astimezone(timezone.utc).isoformat(),
            },
            headers=headers,
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        events.extend(response.json().get('CategoryEvents', []))

    return events


def find_free_rooms(start, end, room_ids):
    rooms = get_events(start, end, room_ids)
    free_rooms = []

    for room in rooms:
        has_overlap = any(
            _as_utc(event['StartDateTime']) < end
            and _as_utc(event['EndDateTime']) > start
            for event in room.get('Results', [])
            if not event.get('IsDeleted', False)
        )
        if not has_overlap:
            free_rooms.append(room['Name'])

    return free_rooms


def main():
    parser = argparse.ArgumentParser(description='Find free timetable rooms.')
    parser.add_argument('date', help='Date in YYYY-MM-DD format.')
    parser.add_argument('start', help='Start time in HH:MM format.')
    parser.add_argument('end', help='End time in HH:MM format.')
    parser.add_argument(
        '--room-id',
        action='append',
        dest='room_ids',
        default=None,
        help='Room identity to search; repeat for multiple rooms.',
    )
    args = parser.parse_args()

    start = datetime.fromisoformat(f'{args.date}T{args.start}').replace(
        tzinfo=timezone.utc
    )
    end = datetime.fromisoformat(f'{args.date}T{args.end}').replace(
        tzinfo=timezone.utc
    )
    if end <= start:
        parser.error('end time must be after start time')

    room_ids = args.room_ids or DEFAULT_ROOM_IDS
    for room in find_free_rooms(start, end, room_ids):
        print(room)


if __name__ == '__main__':
    main()

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"ViewOptions":{"Days":[{"Name":"Monday","DayOfWeek":1,"IsDefault":true},{"Name":"Tuesday","DayOfWeek":2,"IsDefault":true},{"Name":"Wednesday","DayOfWeek":3,"IsDefault":true},{"Name":"Thursday","DayOfWeek":4,"IsDefault":true},{"Name":"Friday","DayOfWeek":5,"IsDefault":true},{"Name":"Saturday","DayOfWeek":6,"IsDefault":true}],"Weeks":[],"TimePeriods":[{"Description":"All Day","StartTime":"00:00","EndTime":"23:59","IsDefault":true}],"DatePeriods":[{"Description":"23/24 All Year","StartDateTime":"2023-08-28T00:00:00+00:00","EndDateTime":"2024-09-01T00:00:00+00:00","IsDefault":true,"Type":null,"Weeks":[]}]},"CategoryTypesWithIdentities":[{"CategoryTypeIdentity":"1e042cb1-547d-41d4-ae93-a1f2c3d34538","CategoryIdentities":["6f5b1e73-04d5-d6d0-49f1-6a15a218056e"]}],"FetchBookings":false,"FetchPersonalEvents":false,"PersonalIdentities":[]}'
#response = requests.post(
#    'https://scientia-eu-v4-api-d4-01.azurewebsites.net/api/Public/CategoryTypes/Categories/Events/Filter/50a55ae1-1c87-4dea-bb73-c9e67941e1fd?startRange=2026-11-10T00:00:00.000Z&endRange=2026-11-13T23:59:59.999Z',
#    headers=headers,
#    data=data,
#)
