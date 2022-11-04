CREATE DEFINER=`root`@`localhost` FUNCTION `setElement`(_key int) RETURNS varchar(10) CHARSET utf8mb4
    DETERMINISTIC
BEGIN

DECLARE _elem varchar(10);
   
   IF MOD(_key,4) = 1 THEN
   SET _elem = 'Fire';
   ELSEIF MOD(_key,4) = 2 THEN
   SET _elem = 'Earth';
   ELSEIF MOD(_key,4) = 3 THEN
   SET _elem = 'Air';
   ELSEIF MOD(_key,4) = 0 THEN
   SET _elem = 'Water';
   ELSE SET _elem = NULL; 
   END IF;
   
RETURN _elem;

END