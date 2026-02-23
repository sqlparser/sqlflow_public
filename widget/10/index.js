$(async () => {
    const $url = $('#url');
    const $tablename = $('#tablename');
    const $columnname = $('#columnname');
    const $visualize = $('#visualize');

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
        const options = {
            url: $url.val(),
            tablename: $tablename.val(),
            columnname: $columnname.val(),
        };

        await sqlflow.visualizeFreestyle(options);
    };

    visualize();

    $visualize.click(visualize);
});
