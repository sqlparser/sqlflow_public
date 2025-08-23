# case expression

## Sample 1
```sql
 select
 	case when a.kamut=1 and b.teur IS null
 			 then 'no locks'
 		 when a.kamut=1
 			then b.teur
 	else 'locks'
 	end teur
 from tbl a left join TT b on (a.key=b.key)
```

During the analyzing of dataflow, case expression is treated as a function. The column used inside the case expression will be treated like the arguments of a function.
So for the above SQL, the following relation is discovered:

```
tbl.kamut -> direct -> teur
TT.teur -> direct -> teur
```

### diagram

![image.png](https://images.gitee.com/uploads/images/2021/0704/140751_da11dcf1_8136809.png)


## Sample 2
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

### diagram
 ![image.png](https://images.gitee.com/uploads/images/2021/0712/183847_efe5301d_8136809.png)