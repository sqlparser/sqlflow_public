$(async () => {
    const $sqltext = $('#sqltext');
    const $visualize = $('#visualize');
    const $error = $('#error');

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

    const visualize = async () => {
        // set sql text property
        sqlflow.sqltext.set($sqltext.val());

        await sqlflow.visualize();

        const error = sqlflow.error.get();
        if (error && error.length > 0) {
            console.log(sqlflow.error.get());
            let text = '';
            error.forEach(item => {
                text += `${item.errorType} : ${item.errorMessage}`;
            });
            $error.val(text);
        } else {
            $error.val('');
        }
    };

    visualize();

    $visualize.click(visualize);
});
