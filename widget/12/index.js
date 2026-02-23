$(async () => {
    //获取url中的参数
    $.getUrlParam = function (name) {
        let reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
        let r = window.location.search.substr(1).match(reg);
        console.log('url', r);
        if (r != null) {
            return unescape(r[2]);
        }
        return null;
    };
    const host = 'http://101.43.7.234:8081';
    const type = $.getUrlParam('type');
    let url = '';
    if (type == 'upstream') {
        url = host + '/gspLive_backend/sqlflow/generation/upstream';
    } else if (type == 'downstream') {
        url = host + '/gspLive_backend/sqlflow/generation/downstream';
    } else {
        return;
    }
    const tablename = $.getUrlParam('table');
    if (tablename === null) {
        return;
    }
    const columnname = $.getUrlParam('column');
    const stopat = $.getUrlParam('stopat');
    const jobid = $.getUrlParam('jobid');
    console.log('url', url);
    console.log('tablename', tablename);
    console.log('columnname', columnname);
    // get a instance of SQLFlow
    const sqlflow = await SQLFlow.init({
        container: document.getElementById('sqlflow'),
        width: '100%',
        height: '100%',
        apiPrefix: 'http://hdp02.sqlflow.cn/api',
        token: '', // input your token
    });

    // set dbvendor property
    sqlflow.vendor.set('oracle');

    const visualize = async () => {
        const options = {
            url,
            tablename,
            columnname,
            jobid,
            stopat,
        };

        await sqlflow.visualizeFreestyle(options);
    };

    visualize();
});
