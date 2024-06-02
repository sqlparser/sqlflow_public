## Integrate Gudu SQLFlow with Datahub

[DataHub](https://datahubproject.io/) is an open-source metadata platform for the modern data stack.

[Gudu SQLFlow](https://sqlflow.gudusoft.com) is a powerful data lineage tool.

Integrate the Gudu SQLFlow with the Datahub enable you easily understand the end-to-end journey of data 
by tracing lineage across platforms, datasets at the column level.

We have built a test envionment so you can see how Gudu SQLFlow works with the Datahub.

### Demo
Please login [Datahub with Gudu SQLFlow](http://101.43.5.98:9002/) with username: datahub, password: datahub

#### 1. After login, just click the dbt icon
<img src="./datahub-sqlflow-dbt.png" alt="datahub-dbt" width="600"/>

#### 2. Select the customer table
<img src="./datahub-sqlflow-dbt-customers.png" alt="datahub-dbt" width="600"/>

#### 3. You will see the Gudu SQLFlow tab
<img src="./datahub-sqlflow-dbt-customers-gudu-sqlflow.png" alt="datahub-dbt" width="600"/>

#### 4. Click the Gudu SQLFlow tab to see the upstream and downstream of this table
<img src="./datahub-sqlflow-dbt-customers-gudu-sqlflow-table-level.png" alt="datahub-dbt" width="600"/>

#### 5. Check the column level lineage by click the lineage item
<img src="./datahub-sqlflow-dbt-customers-gudu-sqlflow-column-level.png" alt="datahub-dbt" width="600"/>

#### 6. See the full column level lineage
<img src="./datahub-sqlflow-dbt-customers-gudu-sqlflow-column-level-result.png" alt="datahub-dbt" width="600"/>


Feel free to [contact us](https://www.gudusoft.com/contact/) if you like to integrate the Gudu SQLFlow into your datahub platform and 
gain the ability to trace column-level data lineage.