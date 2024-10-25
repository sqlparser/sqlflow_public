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
        token: '', // input your token
    });

    // set dbvendor property
    sqlflow.vendor.set('oracle');

    // add an event listener on table click
    sqlflow.addEventListener('onTableNameClick', table => {
        $message.val(JSON.stringify(table));

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
