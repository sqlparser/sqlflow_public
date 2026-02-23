$(async () => {
    //获取url中的参数
    $.getUrlParam = function (name) {
        var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)');
        var search = '&' + window.location.hash.split('?')[1];
        console.log('url', search);
        var r = search.substr(1).match(reg);
        if (r != null) return unescape(r[2]);
        return null;
    };
    const host = 'http://101.43.8.206:8081';
    let url = window.location.href;
    if (url.indexOf('/upstream') >= 0) {
        url = host + '/gspLive_backend/sqlflow/generation/upstream';
    } else if (url.indexOf('/downstream') >= 0) {
        url = host + '/gspLive_backend/sqlflow/generation/downstream';
    } else {
        return;
    }
    const tablename = $.getUrlParam('table');
    if (tablename === null) {
        return;
    }
    const columnname = $.getUrlParam('column');
    console.log('url', url);
    console.log('tablename', tablename);
    console.log('columnname', columnname);
    // get a instance of SQLFlow
    const sqlflow = await SQLFlow.init({
        container: document.getElementById('sqlflow'),
        width: '100%',
        height: '100%',
        apiPrefix: 'http://101.43.8.206/api',
        token: '', // input your token
    });

    // set dbvendor property
    sqlflow.vendor.set('oracle');

    const visualize = async () => {
        const options = {
            url,
            tablename,
            columnname,
            jobid: '',
        };

        await sqlflow.visualizeFreestyle(options);
    };

    visualize();
});
