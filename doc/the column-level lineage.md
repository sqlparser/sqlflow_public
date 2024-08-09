```sql
Insert into enrollment2.EnrollmentCW
SELECT
       CASE WHEN dstf.LastName + ', ' + dstf.FirstName LIKE '%DEFAULT%' THEN ''
            ELSE dstf.LastName + ', ' + dstf.FirstName
       END AS AdvisorFullName,
       CASE WHEN dstf.StaffEmail = 'Unknown' THEN ''
            ELSE dstf.StaffEmail
       END AS AdvisorEmail 
FROM STU_DW.enrollment1.vwStudentEnrollmentCW fsecw
       LEFT JOIN STU_DW.org.DimStaff dstf ON fsecw.DimStaffIDAdvisor = dstf.DimStaffID
                                      AND dstf.IsCurrentRow = 1									  
```


 ![image.png](https://images.gitee.com/uploads/images/2021/0712/183847_efe5301d_8136809.png)

## 1. How to get column-level model from the complete model

## 2. The export format of the column-level model
