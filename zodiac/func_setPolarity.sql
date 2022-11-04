CREATE DEFINER=`root`@`localhost` FUNCTION `setPolarity`(_key int) RETURNS varchar(10) CHARSET utf8mb4
    DETERMINISTIC
BEGIN

DECLARE _pola varchar(10);
   
   IF MOD(_key,2) = 1 THEN
   SET _pola = 'Negative';
   ELSE SET _pola = 'Positive';
   END IF;
   
RETURN _pola;

END