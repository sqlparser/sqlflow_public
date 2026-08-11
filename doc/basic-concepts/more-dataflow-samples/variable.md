### cursor, record variable

This is an Oracle PLSQL.

```sql
DECLARE
	p_run_ind VARCHAR2;
	TYPE acbal_cv IS REF CURSOR;
	rec_dal_acbal T_DAL_ACBAL%ROWTYPE;
BEGIN

IF p_run_ind = 'STEP1' THEN
	OPEN acbal_cv FOR 
		SELECT product_type_code,product_code FROM T_DAL_ACBAL
			WHERE AC_CODE > ' ' AND UPDT_FLG != '0'
			AND UPDAT_FLG != '3' AND ROWNUM < 150001;

ELSIF p_run_ind = 'STEP2' THEN
	OPEN acbal_cv FOR 
		SELECT product_type_code,product_code FROM T_DAL_ACBAL
			WHERE AC_CODE > ' ' AND UPDT_FLG != '0'
			AND UPDAT_FLG != '3';

END IF;

LOOP
	FETCH acbal_cv INTO rec_dal_acbal;
	EXIT WHEN cur_stclerk%NOTFOUND;

	UPDATE T_AC_MSTR
	SET prd_type_code = rec_dal_acbal.product_type_code,
		prd_code = rec_dal_acbal.product_code
	;

END LOOP;

COMMIT;
END;
```

#### dataflow in xml

```xml
<variable id="2" name="acbal_cv" type="variable" subType="cursor" coordinate="[9,7,0],[9,15,0]">
	<column id="14" name="*" coordinate="[1,1,0],[1,2,0]"/>
	<column id="14_0" name="PRODUCT_TYPE_CODE" coordinate="[1,1,0],[1,2,0]"/>
	<column id="14_1" name="PRODUCT_CODE" coordinate="[1,1,0],[1,2,0]"/>
</variable>
<variable id="25" name="rec_dal_acbal" type="variable" subType="record" coordinate="[23,22,0],[23,35,0]">
	<column id="26" name="*" coordinate="[1,1,0],[1,2,0]"/>
	<column id="26_0" name="PRODUCT_TYPE_CODE" coordinate="[1,1,0],[1,2,0]"/>
	<column id="26_1" name="PRODUCT_CODE" coordinate="[1,1,0],[1,2,0]"/>
</variable>
```

#### diagram

![image.png](https://images.gitee.com/uploads/images/2021/0705/110307_74539911_8136809.png)

#### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> `acbal_cv` is a scoped `CURSOR` endpoint and `rec_dal_acbal` is represented by scoped variable/field
> endpoints when identity is proven. SELECT fields flow by VALUE facts into cursor fields, FETCH creates
> VALUE facts into record fields, and those fields flow to the UPDATE targets. IF/WHERE conditions create
> ROW facts; assignments, branches, cursor, record, and loop steps remain in a `ROUTINE_BODY`
> `IntermediateGraph`. The graph reports partial completeness if procedural control flow cannot be fully
> proven.

### scalar variable

This is a Teradata stored procedure

```sql
CREATE PROCEDURE NewProc (IN id CHAR(12),
IN pname INTEGER,
IN pid INTEGER,
OUT dname CHAR(10))
BEGIN

	SELECT AGMT_ID
	INTO dname FROM MY_EPRD2_VR_BASE.AGMT
	WHERE PROCESS_ID = pid;
END;
```

#### dataflow in xml

```xml
<variable id="14" name="dname" type="variable" subType="scalar" coordinate="[8,7,0],[8,12,0]">
	<column id="15" name="dname" coordinate="[8,7,0],[8,12,0]"/>
</variable>
```

#### diagram

![image.png](https://images.gitee.com/uploads/images/2021/0705/110824_924cc303_8136809.png)

#### <span style="color:#8250df">SLPC v0.2 representation</span>

> [!IMPORTANT]
> `id`, `pname`, `pid`, and `dname` are scoped `PARAMETER` endpoints with direction metadata; local `dname`
> may also appear as a VARIABLE node in the routine graph. `AGMT.AGMT_ID -> dname` is `VALUE + DIRECT`,
> while `pid -> predicate` is a parameter VALUE contribution plus `PROCESS_ID -> result rows` as
> `ROW + FILTER`. The OUT parameter/return path remains available to callers through proven parameter
> binding; unresolved call bindings become candidates and diagnostics.
