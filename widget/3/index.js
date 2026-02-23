$(async () => {
    const sqlflow = await SQLFlow.init({
        container: document.getElementById('sqlflow'),
        width: 1000,
        height: 700,
        apiPrefix: 'http://hdp02.sqlflow.cn/api',
        token: '', // input your token
    });

    // view job detail by job id, or leave it empty to view the latest job
    await sqlflow.job.lineage.viewDetailById('fb19960353004c79a966549360c0b8eb');

    sqlflow.job.lineage.selectGraph({
        schema: 'dbsnmp',
        table: 'bsln_baselines',
        column: 'DBID',
    });
});
