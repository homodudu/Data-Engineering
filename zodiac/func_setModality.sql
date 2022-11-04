CREATE DEFINER=`root`@`localhost` FUNCTION `setModality`(_key int) RETURNS varchar(10) CHARSET utf8mb4
    DETERMINISTIC
BEGIN

DECLARE _moda varchar(10);
   
   IF MOD(_key,3) = 2 THEN
   SET _moda = 'Cardinal';
   ELSEIF MOD(_key,3) = 0 THEN
   SET _moda = 'Fixed';
   ELSEIF MOD(_key,3) = 1 THEN
   SET _moda = 'Mutable';
   ELSE SET _moda = NULL; 
   END IF;
   
RETURN _moda;

END