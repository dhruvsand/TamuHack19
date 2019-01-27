import VerificationServiceHttpClientHelper
import sys

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

    print('Enrollments Completed = {0}'.format(enrollment_response.get_enrollments_count()))
    print('Remaining Enrollments = {0}'.format(enrollment_response.get_remaining_enrollments()))
    print('Enrollment Status = {0}'.format(enrollment_response.get_enrollment_status()))
    print('Enrollment Phrase = {0}'.format(enrollment_response.get_enrollment_phrase()))

if __name__ == "__main__":

    key= "82a3a7b473654f27b23ca8f320b855cf"
    profile_id ="3ada7161-c389-4cf4-a51f-e4935e0a27fb"
    path = "./file3.wav"

    # if len(sys.argv) < 4:
    #     print('Usage: python EnrollProfile.py <subscription_key> <profile_id> '
    #         '<enrollment_file_path>')
    #     print('\t<subscription_key> is the subscription key for the service')
    #     print('\t<profile_id> is the profile ID of the profile to enroll')
    #     print('\t<enrollment_file_path> is the enrollment audio file path')
    #
    #     sys.exit('Error: Incorrect Usage.')

    enroll_profile(key, profile_id, path)
