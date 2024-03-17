-- Question 39
select ename, DATE_ADD(hiredate, interval 3 YEAR) from emp
-- Question 40
select *, TIMESTAMPDIFF(
        day, hiredate, CURRENT_TIMESTAMP
    ) as Days
from emp
-- Question 41
select *, TIMESTAMPDIFF(
        month, hiredate, CURRENT_TIMESTAMP
    ) as Months
from emp;
-- select extract(year from curdate()) - extract(year from hiredate)
-- from emp
-- Question 42
select * from emp order by ename;

-- Question 43
select empno, ename, hiredate from emp order by 3;

-- Question 44
select ename, job, sal from emp order by job, sal;

-- Question 45
select ename, job, sal from emp order by job desc, sal;

-- Question 46
select ename, dname, sal
from emp
    join dept on emp.deptno = dept.deptno
where
    TIMESTAMPDIFF(
        year, hiredate, CURRENT_TIMESTAMP
    ) > 1;

-- Question 47
select ename, dname, sal
from emp
    join dept on emp.deptno = dept.deptno
where
    comm = 0
    or comm is NULL
order by dname;

-- Question 48
-- select ename, deptno, hiredate
-- from emp
-- where extract(year from hiredate) = 1981
-- order by hiredate
select ename, dname, hiredate
from emp
    inner join dept on emp.deptno = dept.deptno
where
    year(hiredate) = 1981
order by hiredate;

-- Question 49
select dname, ename
from emp
    right outer join dept on emp.deptno = dept.deptno;

-- Question 50
select DISTINCT
    d.dname,
    m.ename as Boss
from dept d
    left join (
        emp e
        left join emp m on e.mgr = m.empno
    ) on d.deptno = m.deptno;

-- Question 51
select e.ename, e.job, e.sal, manager.ename as Boss
from emp e
    join emp manager on e.mgr = manager.empno;

-- Question 52
select worker.ename
from emp worker, emp manager
where
    worker.mgr = manager.empno
    and worker.sal > manager.sal;

-- Question 53 : Find all the employees who are senior to their bosses.
select e.ename, e.job, e.sal, manager.ename as Boss
from emp e
    join emp manager on e.mgr = manager.empno
where
    TIMESTAMPDIFF(
        day, e.hiredate, manager.hiredate
    ) > 0;

-- Question 54 : Find the names of those employees whose immediate boss is in different department.
select e.ename, e.job, e.sal, manager.ename as Boss, manager.job as Boss_Department
from emp e
    join emp manager on e.mgr = manager.empno
where
    e.job != manager.job;

-- Question 55
select worker.ename, manager.ename as Manager
from emp worker
    left join emp manager on worker.mgr = manager.empno
    -- Question 64
select dname, loc, count(empno), ifnull(round(avg(sal), 2), 0)
from emp
    right outer join dept on emp.deptno = dept.deptno
group by
    dname,
    loc

-- Question 56 : List department number and each distinct pair of employees working in that department.
select e.deptno, e.ename as Employee, manager.ename as Employee2
from emp e
    join emp manager on e.deptno = manager.deptno
where
    e.ename < manager.ename;

-- Question 56 : Display highest, lowest, sum and average salary of all the employees. Round your result to whole numbers.
select
    max(sal) as Max_Salary,
    min(sal) as Min_Salary,
    round(avg(sal)) as Average_Salary
from emp;

-- Question 58 : Display highest, lowest, sum and average salary for each job.
select
    job,
    max(sal) as Max_Salary,
    min(sal) as Min_Salary,
    round(avg(sal)) as Average_Salary
from emp
group by
    job;

-- Question 59 : Count the number of bosses without listing them.
select count(distinct (mgr)) as No_of_Boss from emp;

-- Question 60 : Display the difference between the highest and lowest salary.
select max(sal) - min(sal) as Difference from emp;

-- Question 61 : Display department name and the difference between the highest and lowest salary for that department.
select deptno, max(sal) - min(sal) as Difference
from emp
group by
    deptno;

-- Question 62 : Display department name and average salary for that department.
-- Include only those employees who have joined after 1st July 1981.
select dname, avg(sal)
from emp
    join dept on emp.deptno = dept.deptno
where
    DATEDIFF(hiredate, '1981-7-1') > 0
group by
    dname;

-- Question 63 : Display the  boss and the salary of  lowest paid employee for him. Don’t include minimum salary below Rs. 1000
select manager.ename as Boss, min(e.sal) as Employee_salary
from emp e
    join emp manager on e.mgr = manager.empno
where
    e.sal > 1000
group by
    1

-- Question 64 : Display department name, location name, no. of people working there and average salary. Round average salary to 2 decimal places.
select dname, loc, count(empno), round(avg(sal), 2)
from emp
    right outer join dept on emp.deptno = dept.deptno
group by
    dname,
    loc;

-- Question 65 : Count distinct salary figures and number of employees receiving it.
select sal, count(empno) from emp group by sal;

-- Question 66 : Find all the department details in which at least one employee is working.
select DISTINCT (dept.deptno),
    dname,
    loc
from emp
    LEFT join dept on emp.deptno = dept.deptno;

-- Question 67 : Find all, who are bosses of least one employee.
select distinct (m.empno),
    m.ename
from emp e
    join emp m on e.mgr = m.empno;

-- Question 68 : Find average annual salary of all the employees except analysts.
select avg(sal) * 12 from emp where job != 'Analyst';

-- Question 69 : Create unique listing of all the jobs that are in dept. 30. Include location of the dept. in the output.
select loc, job
from emp
    join dept on emp.deptno = dept.deptno
where
    emp.deptno = 30
group by
    job;

-- Question 70 : List employee name, dept. name, job and location of all employees who work in DALLAS.
select ename, dname, job, loc
from emp
    join dept on emp.deptno = dept.deptno
where
    dept.dname = (
        select dname
        from dept
        where
            loc = 'DALLAS'
    );

-- Question 71 : List  employee name and hiredate of all employees who  are hired after  BLAKE.
select e.ename, e.hiredate
from emp e
where
    e.hiredate > (
        select hiredate
        from emp
        where
            ename = 'Blake'
    );

-- Question 72 : List  employee name , hiredate, manager name, manager’s hiredate   of all employees who  are hired before their managers.
select
    e.ename,
    e.hiredate,
    mng.ename as Manager,
    mng.hiredate as Managers_Hiredate
from emp e
    join emp mng on e.mgr = mng.empno
where
    e.hiredate < mng.hiredate;

-- Question 73 : Display the job and the difference between the highest and the lowest salary for each job.
select job, max(sal) - min(sal) as Diff from emp group by job;

-- Question 74 : Display dept. name, location, no.of employees in the dept. and average salary of the dept. rounded to 2 decima
select DISTINCT (d.dname),
    d.loc,
    count(sal) over (
        PARTITION BY
            d.dname
    ) as count_emp,
    round(
        avg(sal) over (
            PARTITION BY
                d.dname
        ), 2
    ) as average_salary
from emp e
    right outer join dept d on e.deptno = d.deptno

-- Question 75 : List  employee name and hiredate of all employees who  are  in the same  dept. as BLAKE. Exclude BLAKE.
select ename, hiredate
from emp
where
    ename != 'blake'
    and deptno = (
        select deptno
        from emp
        where
            ename = 'blake'
    );

-- Question 76 : Display names and salary of all the employees who report to KING.
select ename, sal
from emp
where
    mgr = (
        select empno
        from emp
        where
            ename = 'King'
    );

-- Question 77 : Write a query to display name, dept. no, and salary of any employee whose  is not located at DALLAS  but his/her salary and commission match with the   salary and commission of at least one  employee located in DALLAS.
select ename, dept.deptno, sal
from emp
    join dept on emp.deptno = dept.deptno
where
    loc != 'dallas'
    and (sal, comm) = ANY (
        select sal, comm
        from emp
            join dept on emp.deptno = dept.deptno
        where
            loc = 'dallas'
    );

-- Question 78 : Display name , hire date and salary of all the employees who have both salary and commission same as SCOTT. Donot include Scott in the list.
select ename, hiredate, sal
from emp
where
    ename != 'Scott'
    and (sal, IFNULL(comm, 0)) = (
        select sal, IFNULL(comm, 0)
        from emp
        where
            ename = 'scott'
    );

-- Question 79 : List employees who earn salary higher than the highest salary of clerks.
select *
from emp
where
    sal > (
        select max(sal)
        from emp
        where
            job = 'Clerk'
    );

-- Question 80 : List employees whose  salary is higher than the average salary of employees in department no. 10.
select *
from emp
where
    sal > (
        select avg(sal)
        from emp
        where
            deptno = 10
    );

-- Question 81 : Display  the names of employees who are earning minimum and maximum salary in one line.
select a.ename as Max, b.ename as Min
from (
        select ename
        from emp
        where
            sal = (
                select max(sal)
                from emp
            )
    ) a, (
        select ename
        from emp
        where
            sal = (
                select min(sal)
                from emp
            )
    ) b;

-- Question 82 : Find out top 4 salaries of the company. Display their rank as well.
select *, row_number() over (
        order by sal desc
    ) as rank_emp
from emp
limit 4

-- Question 83 : Find out earliest 3 employees who have joined the company. Display their rank as well.
select *, row_number() over (
        order by year(hiredate) desc
    ) as rank_emp
from emp e
limit 4

-- Question 84 : Print employee name, salary and average salary of his department.
select ename, sal, round(
        avg(sal) over (
            order by deptno
        ), 2
    ) as Average_Salary
from emp;

-- Question 85 : Display ename, department name and grade of each employee who joined the organization before their boss.
with
    grade_table as (
        select empno, grade
        from emp, salgrade
        where
            sal between losal and hisal
    )
select e.ename, dname, grade
from
    emp e
    join emp mng
    join dept
    join grade_table g on e.mgr = mng.empno
    and e.empno = g.empno
    and e.deptno = dept.deptno
where
    e.hiredate < mng.hiredate;

-- Question 86 : Display each deprtment name and the first employee who joined that department.
select dname, ename
from dept
    left outer join emp e on e.deptno = dept.deptno
where (dept.deptno, e.hiredate) = ANY (
        select deptno, min(hiredate)
        from emp
        group by
            deptno
    );

-- Question 87 : How much more salary Miller needs to earn to be in King’s grade?
-- select losal - sal
-- from (
--         select losal
--         from emp
--             join salgrade
--         where
--             emp.sal > salgrade.losal
--             and emp.sal < salgrade.hisal
--             and ename = 'KING'
--     ) a, (
--         select sal
--         from emp
--         where
--             ename = 'miller'
--     ) b;
-- Using CTE
with
    kings_sal as (
        select losal
        from emp
            join salgrade on sal BETWEEN losal and hisal
        where
            ename = 'King'
    )
select losal - sal
from emp
    join kings_sal
where
    ename = 'miller';

-- Question 88 : Display employees who joined in the last month(1st day of last month – Last day of last month). Do not hardcode the month name.

-- Question 89 : How much more salary does each person need to earn to go in the next grade?
with
    grade as (
        select empno, hisal
        from emp
            join salgrade
        where
            sal between losal and hisal
    )
select
    ename,
    hisal - sal + 1 as Upgrade_required
from emp
    join grade
where
    emp.empno = grade.empno;



-- Question 90 : List different locations from where employees are reporting to King.
select loc
from emp
    join dept on emp.deptno = dept.deptno
where
    emp.mgr = (
        select empno
        from emp
        where
            ename = 'King'
    );

-- Question 91 : List different grades of employees working in ‘DALLAS’
select loc
from emp e
    join emp mng
    join dept on e.mgr = mng.empno
    and e.deptno = dept.deptno
where
    mng.ename = 'King';

-- Question 92 : Display grade 2 employees in Finance department who will complete 3 years in March this year.
select ename
from emp
    join salgrade
    join dept
where
    sal between losal and hisal
    and emp.deptno = dept.deptno
    and dname = 'Finance'
    and TIMESTAMPDIFF(year, hiredate, '2024-3-31') = 3;

-- Question 93 : Display employees who are earning salary more than the average salary of employees in the same grade.
select *
from emp outer1
where
    outer1.sal > (
        select avg(sal)
        from emp inner1
        where (
                select grade
                from salgrade
                where
                    inner1.sal BETWEEN losal and hisal
            ) = (
                select grade
                from salgrade
                where
                    outer1.sal BETWEEN losal and hisal
            )
    );

-- Question 94 : Display employees who are in that same grade as Miller and do not belong to the place which Miller belongs to.
with
    emp_grade as (
        select ename, loc, grade
        from emp
            join dept
            join salgrade on emp.deptno = dept.deptno
        where
            sal between losal and hisal
    )
select DISTINCT (emp1.ename)
from emp_grade emp1
    join emp_grade emp2
where
    emp1.grade = emp2.grade
    and emp1.loc != emp2.loc
    and emp2.ename = 'Miller';

-- Question 95 : How many employees are there between the highest grade of a clerk and the lowest grade of a manager?
select count(e.ename) as Count
FROM emp e
where (
        select grade
        from salgrade
        where
            e.sal between losal and hisal
    ) between (
        select min(grade)
        from salgrade
            join emp
        where
            sal between losal and hisal
            and job = 'Manager'
    ) and (
        select max(grade)
        from emp
            join salgrade
        where
            sal between losal and hisal
            and job = 'Clerk'
    )

-- Question 96 : List analysts and clerks who are either staying at Chicago or Boston and in grade 3 and above.
with emp_grade as (
    select grade, empno
    from salgrade, emp
    where sal BETWEEN losal and hisal
)
select *
from emp,dept,emp_grade
where emp.deptno = dept.deptno and emp_grade.empno = emp.empno and (loc = 'Chicago' or loc = 'Boston') and emp_grade.grade >= 3;