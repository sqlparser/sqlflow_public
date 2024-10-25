document.addEventListener('DOMContentLoaded', async () => {
    const $login = $('#login');
    const $signup = $('#signup');

    // http://127.0.0.1:8260/#/
    // https://sqlflow.gudusoft.com/#/?

    const auth0RedirectUri = 'https://sqlflow.gudusoft.com/#/?';

    const auth0 = new window.auth0.WebAuth({
        domain: 'login.gudusoft.com',
        clientID: 'PZ7fv0vKLL8f0HFW0FIlP1PiDeF0h5HD',
        redirectUri: auth0RedirectUri,
        scope: 'openid profile email',
        overrides: {
            __tenant: 'gudusoft',
            __token_issuer: 'https://login.gudusoft.com/',
        },
    });

    const getUrl = initial_screen => {
        const url = auth0.client.buildAuthorizeUrl({
            redirectUri: auth0RedirectUri,
            responseType: 'id_token',
            state: '123',
            nonce: '123',
            initial_screen,
        });

        return url;
    };

    const login = () => {
        location.href = getUrl('login');
    };

    const signup = () => {
        location.href = getUrl('signUp');
    };

    $login.click(login);

    $signup.click(signup);
});
