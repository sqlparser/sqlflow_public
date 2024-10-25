document.addEventListener('DOMContentLoaded', async () => {
    const sqlflow = await SQLFlow.init({
        container: document.getElementById('sqlflow'),
        width: '100%',
        height: '100%',
    });

    await sqlflow.visualizeJSON(window.data);
});
