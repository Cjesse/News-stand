class Auth {
	/* authenticate a user. Save a token string in local storage
	* @param {string} token
	* @param {string} email
	*/
	static authenticateUser(token, email) {
		localStorage.setItem('token', token);
		localStorage.setItem('email', email);
	}

	/**
	* check if a user is authenticated = check if a token is saved in local storage
	*
	* @return {boolean}
	*/
	static isUserAuthenticated() {
		return localStorage.getItem('token') != null;
	}

	/**
	* deauthenticate a user. Remove token and email from local storage
	*/
	static deauthenticateUser() {
		localStorage.removeItem('token');
		localStorage.removeItem('email');
	}

	/**
	* Get a token value.
	*
	* @return {string}
	*/
	static getToken() {
		return localStorage.getItem('token');
	}

	/**
	* Get email
	*
	* @return {string}
	*/
	static getEmail() {
		return localStorage.getItem('email');
	}
}

export default Auth;