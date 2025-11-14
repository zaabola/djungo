--set serveroutput on
/*
BEGIN

dbms_output.put_line('Hello world');

END;
/

DECLARE

v_msg varchar2(20) := 'Hello world';

BEGIN

--v_msg := 'Hello world';
dbms_output.put_line(v_msg);

END;
/



--ecrire un bloc anonyme permettant d'afficher le nom de l'employee ayant un id=124
DECLARE

v_nom varchar2(30);
v_prenom varchar2(30);

BEGIN

SELECT last_name , first_name INTO v_nom , v_prenom FROM employees where employee_id=124;

dbms_output.put_line(v_nom);
dbms_output.put_line(v_prenom);
dbms_output.put_line('lemployee est :' || v_nom || ' ' || v_prenom);

END;
/


DECLARE

v_nom employees.last_name%TYPE; --pour recuperer le longeur de le type

BEGIN

SELECT last_name INTO v_nom FROM employees where employee_id=124;

dbms_output.put_line(v_nom);
END;
/


DECLARE

v_emp employees%ROWTYPE;

BEGIN

SELECT * INTO v_emp FROM employees where employee_id=124;

dbms_output.put_line(v_emp.last_name || ' ' || v_emp.first_name);

END;
/


DECLARE

TYPE type_emp IS RECORD
(last_name employees.last_name%TYPE , salary employees.salary%TYPE);
v_emp type_emp ;

BEGIN

SELECT last_name , salary INTO v_emp FROM employees where employee_id=124;
dbms_output.put_line(v_emp.last_name || ' ' || v_emp.salary);

END;
/

--ecrire un bloc permettant de comparer deux entiers v1 et v2
DECLARE

v1 integer := &v1;
v2 integer :=&v2;

BEGIN

IF (v1 > v2) THEN
dbms_output.put_line(v2 || ' < ' || v1);
ELSE
dbms_output.put_line(v2 || ' >= ' || v1);
END IF;

END;
/

--case
DECLARE

v integer :=&v;

BEGIN

CASE v
when 1 then dbms_output.put_line('A');
when 2 then dbms_output.put_line('B');
when 3 then dbms_output.put_line('C');
else dbms_output.put_line('X');
END CASE;
END;
/

DECLARE

v integer :=&v;

BEGIN

CASE
when v<5 then dbms_output.put_line('A');
when v<10 then dbms_output.put_line('B');
when v<15 then dbms_output.put_line('C');
else dbms_output.put_line('X');
END CASE;

END;
/

DECLARE
    v_counter INTEGER := 1;
BEGIN
WHILE v_counter <= 10 LOOP
DBMS_OUTPUT.PUT_LINE(v_counter);
v_counter := v_counter + 1;
END LOOP;

END;
/

DECLARE
    v_counter INTEGER := 1;
BEGIN
    LOOP
        DBMS_OUTPUT.PUT_LINE(v_counter);
        v_counter := v_counter + 1;
        EXIT WHEN (v_counter = 11);
    END LOOP;
END;
/

DECLARE
    v_counter INTEGER := 1;
BEGIN
    for v_counter in 1 .. 10
    LOOP
        DBMS_OUTPUT.PUT_LINE(v_counter);
    END LOOP;
END;
/
*/
