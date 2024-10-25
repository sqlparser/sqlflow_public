$(async () => {
    const $sqltext = $('#sqltext');
    const $visualize = $('#visualize');
    const $message = $('#message');

    // get a instance of SQLFlow
    const sqlflow = await SQLFlow.init({
        container: document.getElementById('sqlflow'),
        width: 1000,
        height: 400,
        apiPrefix: 'http://hdp02.sqlflow.cn/api',
        userId: '21232f297a57a5a743894a0e4a801fc3',
        token: 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJnYW8gYXQgaG9tZSIsImV4cCI6MTcxNTg3NTIwMCwiaWF0IjoxNjg0MzM5MjAwfQ.Bjug3RqUyx-ay4t2XLnX0OJoaa5pMH0qme8RXMEjTLE', // input your token
    });

    // set dbvendor property
    sqlflow.vendor.set('oracle');

    // add an event listener on field(column) click
    sqlflow.addEventListener('onFieldClick', field => {
        $message.val(JSON.stringify(field));

        // remove all event listeners
        // sqlflow.removeAllEventListener()
    });

    const visualize = async () => {
        // set sql text property
        sqlflow.sqltext.set($sqltext.val());

        await sqlflow.visualize();
    };

    visualize();

    $visualize.click(visualize);
});
