$(async () => {
    const $sqltext = $('#sqltext');
    const $dataflow = $('#dataflow');
    const $impact = $('#impact');
    const $recordset = $('#recordset');
    const $function = $('#function');
    const $visualize = $('#visualize');
    const $file = $('#file');

    // get a instance of SQLFlow
    const sqlflow = await SQLFlow.init({
        container: document.getElementById('sqlflow'),
        width: 1000,
        height: 800,
        apiPrefix: 'http://hdp02.sqlflow.cn/api',
        token: '', // input your token
    });

    // set dbvendor property
    sqlflow.vendor.set('oracle');

    const visualize = async () => {
        // set sql text property
        sqlflow.sqltext.set($sqltext.val());

        // set default options
        $recordset.prop('checked', true);
        $dataflow.prop('checked', true);
        $impact.prop('checked', false);
        $function.prop('checked', false);

        sqlflow.visualize();
    };

    $file.on('change', async e => {
        const file = $file.prop('files')[0];
        const content = await file.text();
        $sqltext.val(content);
        visualize();
    });

    $visualize.click(visualize);

    $dataflow.change(() => {
        const checked = $dataflow.prop('checked');
        sqlflow.setting.dataflow.set(checked);
    });

    $impact.change(() => {
        const checked = $impact.prop('checked');
        sqlflow.setting.impact.set(checked);
    });

    $recordset.change(() => {
        const checked = $recordset.prop('checked');
        sqlflow.setting.showIntermediateRecordset.set(checked);
    });

    $function.change(() => {
        const checked = $function.prop('checked');
        sqlflow.setting.showFunction.set(checked);
    });
});
