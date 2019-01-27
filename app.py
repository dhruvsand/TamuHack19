import json
import wave
from functools import wraps
import VerificationServiceHttpClientHelper
import pyaudio
from auth0.v3.authentication import Passwordless
from authlib.flask.client import OAuth
from flask import Flask
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from six.moves.urllib.parse import urlencode
import http.client
import csv

app = Flask(__name__)
app.secret_key='qQENIr2ahfnWMcKO28jS0ejJ5so4iSV1FPlZN863LD4Tbp0MiKk1zERp90bt-Zap'


with open('dict.csv') as csv_file:
    reader = csv.reader(csv_file)
    myDict = dict(reader)

profileID =''
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 7
WAVE_OUTPUT_FILENAME = "file1.wav"


oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id='RLGBKFxPCJ4dByOY5N7QcMH77dy3Y5ex',
    client_secret='qQENIr2ahfnWMcKO28jS0ejJ5so4iSV1FPlZN863LD4Tbp0MiKk1zERp90bt-Zap',
    api_base_url='https://tamuhack19.auth0.com',
    access_token_url='https://tamuhack19.auth0.com/oauth/token',
    authorize_url='https://tamuhack19.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)


passwordless = Passwordless("tamuhack19.auth0.com")


# /server.py

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/login')
    return f(*args, **kwargs)

  return decorated


@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('hello_world', _external=True), 'client_id': 'RLGBKFxPCJ4dByOY5N7QcMH77dy3Y5ex'}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

# /server.py

@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))


@app.route('/')
def hello_world():
    return render_template('home.html')


# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    idmy= userinfo['sub']

    conn = http.client.HTTPSConnection("tamuhack19.auth0.com")

    headers = {
        'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik56bEZORFl6TVVVMlJqQTRORGczUTBJNFJqUTBRamN3TmtReE5VTkZNME13TTBWRU9USXpSUSJ9.eyJpc3MiOiJodHRwczovL3RhbXVoYWNrMTkuYXV0aDAuY29tLyIsInN1YiI6IkhOWDBNQ1ZPOFR6WEo2U2tjcWRzNm1TdzVCQThtYVA3QGNsaWVudHMiLCJhdWQiOiJodHRwczovL3RhbXVoYWNrMTkuYXV0aDAuY29tL2FwaS92Mi8iLCJpYXQiOjE1NDg1ODgzNjUsImV4cCI6MTU0ODY3NDc2NSwiYXpwIjoiSE5YME1DVk84VHpYSjZTa2NxZHM2bVN3NUJBOG1hUDciLCJzY29wZSI6InJlYWQ6Y2xpZW50X2dyYW50cyBjcmVhdGU6Y2xpZW50X2dyYW50cyBkZWxldGU6Y2xpZW50X2dyYW50cyB1cGRhdGU6Y2xpZW50X2dyYW50cyByZWFkOnVzZXJzIHVwZGF0ZTp1c2VycyBkZWxldGU6dXNlcnMgY3JlYXRlOnVzZXJzIHJlYWQ6dXNlcnNfYXBwX21ldGFkYXRhIHVwZGF0ZTp1c2Vyc19hcHBfbWV0YWRhdGEgZGVsZXRlOnVzZXJzX2FwcF9tZXRhZGF0YSBjcmVhdGU6dXNlcnNfYXBwX21ldGFkYXRhIGNyZWF0ZTp1c2VyX3RpY2tldHMgcmVhZDpjbGllbnRzIHVwZGF0ZTpjbGllbnRzIGRlbGV0ZTpjbGllbnRzIGNyZWF0ZTpjbGllbnRzIHJlYWQ6Y2xpZW50X2tleXMgdXBkYXRlOmNsaWVudF9rZXlzIGRlbGV0ZTpjbGllbnRfa2V5cyBjcmVhdGU6Y2xpZW50X2tleXMgcmVhZDpjb25uZWN0aW9ucyB1cGRhdGU6Y29ubmVjdGlvbnMgZGVsZXRlOmNvbm5lY3Rpb25zIGNyZWF0ZTpjb25uZWN0aW9ucyByZWFkOnJlc291cmNlX3NlcnZlcnMgdXBkYXRlOnJlc291cmNlX3NlcnZlcnMgZGVsZXRlOnJlc291cmNlX3NlcnZlcnMgY3JlYXRlOnJlc291cmNlX3NlcnZlcnMgcmVhZDpkZXZpY2VfY3JlZGVudGlhbHMgdXBkYXRlOmRldmljZV9jcmVkZW50aWFscyBkZWxldGU6ZGV2aWNlX2NyZWRlbnRpYWxzIGNyZWF0ZTpkZXZpY2VfY3JlZGVudGlhbHMgcmVhZDpydWxlcyB1cGRhdGU6cnVsZXMgZGVsZXRlOnJ1bGVzIGNyZWF0ZTpydWxlcyByZWFkOnJ1bGVzX2NvbmZpZ3MgdXBkYXRlOnJ1bGVzX2NvbmZpZ3MgZGVsZXRlOnJ1bGVzX2NvbmZpZ3MgcmVhZDplbWFpbF9wcm92aWRlciB1cGRhdGU6ZW1haWxfcHJvdmlkZXIgZGVsZXRlOmVtYWlsX3Byb3ZpZGVyIGNyZWF0ZTplbWFpbF9wcm92aWRlciBibGFja2xpc3Q6dG9rZW5zIHJlYWQ6c3RhdHMgcmVhZDp0ZW5hbnRfc2V0dGluZ3MgdXBkYXRlOnRlbmFudF9zZXR0aW5ncyByZWFkOmxvZ3MgcmVhZDpzaGllbGRzIGNyZWF0ZTpzaGllbGRzIGRlbGV0ZTpzaGllbGRzIHVwZGF0ZTp0cmlnZ2VycyByZWFkOnRyaWdnZXJzIHJlYWQ6Z3JhbnRzIGRlbGV0ZTpncmFudHMgcmVhZDpndWFyZGlhbl9mYWN0b3JzIHVwZGF0ZTpndWFyZGlhbl9mYWN0b3JzIHJlYWQ6Z3VhcmRpYW5fZW5yb2xsbWVudHMgZGVsZXRlOmd1YXJkaWFuX2Vucm9sbG1lbnRzIGNyZWF0ZTpndWFyZGlhbl9lbnJvbGxtZW50X3RpY2tldHMgcmVhZDp1c2VyX2lkcF90b2tlbnMgY3JlYXRlOnBhc3N3b3Jkc19jaGVja2luZ19qb2IgZGVsZXRlOnBhc3N3b3Jkc19jaGVja2luZ19qb2IgcmVhZDpjdXN0b21fZG9tYWlucyBkZWxldGU6Y3VzdG9tX2RvbWFpbnMgY3JlYXRlOmN1c3RvbV9kb21haW5zIHJlYWQ6ZW1haWxfdGVtcGxhdGVzIGNyZWF0ZTplbWFpbF90ZW1wbGF0ZXMgdXBkYXRlOmVtYWlsX3RlbXBsYXRlcyByZWFkOm1mYV9wb2xpY2llcyB1cGRhdGU6bWZhX3BvbGljaWVzIHJlYWQ6cm9sZXMgY3JlYXRlOnJvbGVzIGRlbGV0ZTpyb2xlcyB1cGRhdGU6cm9sZXMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.4JPFnSShSnTtSmtpHh5LptvHgtH6POvJSYbdo-wG2nnEvoVAdW6MiGGfj5bBYngbjsuSryGG8DTI0jYSBWbfyD6z_lifuZfQCRSQXlIZltbt1x6Op0yRRmoldR0TMmeXlivNXi5pvcwaQ4zfFYSg-l_e1yL6WECAHyjx5hEkBOyZ0c_1e6Li3XCh1ZJyjXGq8pxF7djfaMOAn7ryFP5etpDaUqdRqYuNGbZh1M5SBkfZvRRhaDU3D1WEQyto8tBlvxT16kqEMwrpeMavBHfIgCpKifFyDskYLfghaSlNioRDqbldYMdcszUVyWNfVd4O4qG3jsz9g2OSkgF9OnSZzA"}

    conn.request("GET", "/api/v2/users/"+idmy, headers=headers)

    res = conn.getresponse()
    data = res.read()

    loginNum= data.decode("utf-8").split(':')[-1].replace('}','')

    print(loginNum)

    global myDict
    global profileID
    if (idmy not in myDict):
        profileID = create_profile("82a3a7b473654f27b23ca8f320b855cf", 'en-us')

        myDict[idmy] = profileID

        with open('dict.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            for key, value in myDict.items():
                writer.writerow([key, value])

        return redirect('/register1Voice')

    profileID = myDict[idmy]
    return redirect('/validateVoice')



@app.route('/login')
def login():

    # return passwordless.email(client_id="RLGBKFxPCJ4dByOY5N7QcMH77dy3Y5ex",email="dhruvsand@yahoo.com")

    return auth0.authorize_redirect(redirect_uri='http://127.0.0.1:5000/callback', audience='https://tamuhack19.auth0.com/userinfo')




@app.route("/record/", methods=['POST'])
def record():
    render_template('record.html', forward_message="Recording ...")
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    return render_template('record.html',forward_message="Done Recording")





@app.route("/Vrecord/", methods=['POST'])
def Vrecord():
    render_template('validate.html', forward_message="Recording ...")
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    return render_template('validate.html',forward_message="Done Recording")







@app.route("/upload/", methods=['POST'])
def upload():
    str = enroll_profile("82a3a7b473654f27b23ca8f320b855cf", profileID, "./file1.wav")

    if"Repeat This 0" in str :
        return redirect('/validateVoice')

    return render_template('record.html',forward_message=str)





@app.route("/Vupload/", methods=['POST'])
def Vupload():
    str = verify_file("82a3a7b473654f27b23ca8f320b855cf", "./file1.wav", profileID)

    if"Verification Result = Accept" in str :
        return redirect('/dashboard')

    return render_template('validate.html',forward_message=str)





@app.route('/register1Voice')
def register1():

    return render_template('record.html')

@app.route('/validateVoice')
def validate1():
    return render_template('validate.html')



if __name__ == '__main__':
    app.run()






def create_profile(subscription_key, locale):
    """Creates a profile on the server.

    Arguments:
    subscription_key -- the subscription key string
    locale -- the locale string
    """
    helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(
        subscription_key)

    creation_response = helper.create_profile(locale)

    return creation_response.get_profile_id()

def enroll_profile(subscription_key, profile_id, file_path):
    """Enrolls a profile on the server.

    Arguments:
    subscription_key -- the subscription key string
    profile_id -- the profile ID of the profile to enroll
    file_path -- the path of the file to use for enrollment
    """
    helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(
        subscription_key)

    enrollment_response = helper.enroll_profile(profile_id, file_path)

    str =""
    str+='Enrollments Completed = {0}'.format(enrollment_response.get_enrollments_count())+"\n"
    str+='Repeat This {0} more times'.format(enrollment_response.get_remaining_enrollments())+"\n"
    str+='Enrollment Status = {0}'.format(enrollment_response.get_enrollment_status())+"\n"
    str+='Enrollment Phrase = {0}'.format(enrollment_response.get_enrollment_phrase())+"\n"


    print('Enrollments Completed = {0}'.format(enrollment_response.get_enrollments_count()))
    print('Remaining Enrollments = {0}'.format(enrollment_response.get_remaining_enrollments()))
    print('Enrollment Status = {0}'.format(enrollment_response.get_enrollment_status()))
    print('Enrollment Phrase = {0}'.format(enrollment_response.get_enrollment_phrase()))
    return str

def verify_file(subscription_key, file_path, profile_id):
    """verify a profile based on submitted audio sample

    Arguments:
    subscription_key -- the subscription key string
    file_path -- the audio file path for verification
    profile_id -- ID of a profile to attempt to match the audio sample to
    """
    helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(
        subscription_key)
    verification_response = helper.verify_file(file_path, profile_id)

    str = 'Verification Result = {0}'.format(verification_response.get_result()) + '\n'
    str+= 'Confidence = {0}'.format(verification_response.get_confidence())

    print('Verification Result = {0}'.format(verification_response.get_result()))
    print('Confidence = {0}'.format(verification_response.get_confidence()))

    return str