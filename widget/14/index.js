document.addEventListener('DOMContentLoaded', async () => {
    Vue.component('sqlflow', {
        template: '<div ref="el"></div>',

        async mounted() {
            // get a instance of SQLFlow
            const sqlflow = await SQLFlow.init({
                container: this.$refs.el, // get element ref from vue
                width: 1000,
                height: 315,
                apiPrefix: 'http://hdp02.sqlflow.cn/api',
                token: '', // input your token
            });

            // set dbvendor property
            sqlflow.vendor.set('oracle');

            // set sql text property
            sqlflow.sqltext.set(`CREATE VIEW vsal
                    AS
                      SELECT a.deptno                  "Department",
                             a.num_emp / b.total_count "Employees",
                             a.sal_sum / b.total_sal   "Salary"
                      FROM   (SELECT deptno,
                                     Count()  num_emp,
                                     SUM(sal) sal_sum
                              FROM   scott.emp
                              WHERE  city = 'NYC'
                              GROUP  BY deptno) a,
                             (SELECT Count()  total_count,
                                     SUM(sal) total_sal
                              FROM   scott.emp
                              WHERE  city = 'NYC') b
                    ;`);

            sqlflow.visualize();
        },
    });

    var app = new Vue({
        el: '#sqlflow',
        template: '<sqlflow />',
    });
});
