import VerificationServiceHttpClientHelper
import sys

def reset_enrollments(subscription_key, profile_id):
	"""Reset enrollments of a given profile from the server
	
    Arguments:
    subscription_key -- the subscription key string
    profile_id -- the profile ID of the profile to reset
	"""
	
	helper = VerificationServiceHttpClientHelper.VerificationServiceHttpClientHelper(subscription_key)
	
	helper.reset_enrollments(profile_id)
	
	print('Profile {0} has been successfully reset.'.format(profile_id))
	
	
	
if __name__ == "__main__":
	key = "82a3a7b473654f27b23ca8f320b855cf"
	profile_id = "3ada7161-c389-4cf4-a51f-e4935e0a27fb"

	# if len(sys.argv) < 3:
	# 	print('Usage: python ResetEnrollments.py <subscription_key> <profile_id> ')
	# 	print('\t<subscription_key> is the subscription key for the service')
	# 	print('\t<profile_id> the ID for a profile to reset its enrollments')
	# 	sys.exit('Error: Incorrect usage.')
	
	reset_enrollments(key,profile_id)
	
