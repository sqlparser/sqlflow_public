let  sqlflow = null;

document.addEventListener('DOMContentLoaded', async () => {
    sqlflow = await SQLFlow.init({
        container: document.getElementById('sqlflow'),
        width: '100%',
        height: '100%',
        component: {
            sqlEditor: true,
            graphLocate: true,
            minimap: true,
        },
    });
    sqlflow.vendor.set("dbvoracle");
});

const visualize = async () => {
    let text = sqlflow.sqltext.get();
    let json = JSON.parse(text);
    await sqlflow.visualizeJSON(json, { layout: true });
};