import VerificationServiceHttpClientHelper
import sys

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
    print('Verification Result = {0}'.format(verification_response.get_result()))
    print('Confidence = {0}'.format(verification_response.get_confidence()))

if __name__ == "__main__":

    key= "82a3a7b473654f27b23ca8f320b855cf"
    profile_id ="3ada7161-c389-4cf4-a51f-e4935e0a27fb"
    path = "./file4true.wav"

    # if len(sys.argv) < 4:
    #     print('Usage: python VerifyFile.py <subscription_key> <verification_file_path>'
    #           ' <profile_id>...')
    #     print('\t<subscription_key> is the subscription key for the service')
    #     print('\t<verification_file_path> is the audio file path for verification')
    #     print('\t<profile_id> the ID for a profile to verify as the user using the submitted audio sample')
    #     sys.exit('Error: Incorrect Usage.')

    verify_file(key,path, profile_id)
