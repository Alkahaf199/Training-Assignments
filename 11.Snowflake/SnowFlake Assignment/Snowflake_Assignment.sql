Drive Link: https://drive.google.com/drive/u/0/folders/1UJU1SZhPXDfnE1kuYZqMDq-wMTbBH9Em

Producer Side

1. Create a sharing link :
   CREATE share <share_name>;
2. Add account to the link : 
   alter share <share_name> 
   add account= rkzdgra.yk91367; // mention the receiver’s ID
3. Create a role
   create database role <role_name>;
4. Grant access to the database to the role : 
   grant usage on database <database_name> to share s1;
   grant usage on schema PUBLIC to share <share_name>;
   grant select on view <view_name> to database role <role_name>;
   grant database role <role_name> to share <share_name>;
   GRANT select on all tables in schema public to share <share_name>;

Consumer Side 

1. See all the sharing link :
   show shares;
2. View accessed database :
   show databases;
3. Create database from the shared channel : 
   create database <new_database_name> from share <producer_id>.<share_name>;
4. Show tables;

