from db.db_connection import conn
import datetime
import re

class OverlapException(Exception):
    pass


def is_email_valid(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False
    
def is_phone_valid(s):
    Pattern = re.compile("(0|91)?[6-9][0-9]{9}")
    return Pattern.match(s)

def validate_payload(data):
    if not data.get('email') or not data.get("phoneNumber"):
        return False
    if not is_email_valid(data.get('email')):
        return False
    if not is_phone_valid(data.get("phoneNumber")):
        return False
    
    return True


def get_id(data):
    temp=set()
    for s, p in data:
        temp.add(p or s)
    return list(temp)

def get_contacts(phone, email):
    query=f"SELECT id, linkedId from Contact WHERE phoneNumber = '{phone}' or email = '{email}'"
    
    cur = conn.cursor()
    cur.execute(query)
    res= cur.fetchall()

    if res:
        id = get_id(res)
        if len(id)>1:
            raise OverlapException("Contact Overlap!")
        query=f"SELECT id, linkedId, phoneNumber, email, linkedPrecedence from Contact WHERE linkedId = '{id[0]}' or id = '{id[0]}'"
        print(query, res)
        cur.execute(query)
        res = cur.fetchall()

        cur.close()
        return res
        
    else:
        return []

def create_new_contact(phone, email, linkedPrecedence='primary'):
    query=f"INSERT INTO Contact (phoneNumber, email, linkedPrecedence) VALUES ('{phone}' , '{email}', '{linkedPrecedence}')"
    cur = conn.cursor()
    cur.execute(query)
    cur.execute('SELECT LASTVAL()')
    inserted_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    print("new contact created")
    return inserted_id


def filter_contacts(data):
    temp=set()
    primary_contact=None
    payload={
        "primaryContactId":None,
        "emails": set(),
        "phoneNumbers": set(),
        "secondaryContactIds": set()
    }
    for d in data:
        if d[-1]=='secondary':
            temp.add(d[1])
            payload['secondaryContactIds'].add(d[0])

        else:
            temp.add(d[0])
            payload['primaryContactId']=d[0]
            primary_contact=d
        
        
        payload['emails'].add(d[3])
        payload['phoneNumbers'].add(d[2])
    
    
    return primary_contact, payload


def identify_data(email, phone):

    existing_contact = get_contacts(phone, email)
    if not existing_contact:
        inserted_id = create_new_contact(phone, email)
        return True, {
        "primaryContactId":inserted_id,
        "emails": [email],
        "phoneNumbers": [phone],
        "secondaryContactIds": []
    }

    else:
        primary_contact, payload = filter_contacts(existing_contact)

        if phone==primary_contact[2] and email==primary_contact[3]:
            payload['emails']=list(payload['emails'])
            payload['phoneNumbers']=list(payload['phoneNumbers'])
            payload['secondaryContactIds']=list(payload['secondaryContactIds'])
        
            return False, payload
        else:
            
            cur=conn.cursor()
            query=f"INSERT INTO Contact (phoneNumber, email, linkedId, linkedPrecedence) VALUES ('{primary_contact[2]}' , '{primary_contact[3]}', '{primary_contact[0]}', 'secondary')"
            cur.execute(query)
            cur.execute('SELECT LASTVAL()')
            inserted_id=cur.fetchone()[0]
            query=f"UPDATE Contact SET phoneNumber = '{phone}', email = '{email}', updatedAt = '{datetime.datetime.now()}' WHERE id = {primary_contact[0]}"                
            cur.execute(query)
            conn.commit()
            cur.close()

            payload['emails'].add(email)
            payload['phoneNumbers'].add(phone)
            payload['secondaryContactIds'].add(inserted_id)

            payload['emails']=list(payload['emails'])
            payload['phoneNumbers']=list(payload['phoneNumbers'])
            payload['secondaryContactIds']=list(payload['secondaryContactIds'])
        
        return True, payload



