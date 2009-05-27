delimiter //
CREATE DEFINER=`yuki`@`localhost` PROCEDURE `replace_markov`(IN nows VARCHAR(32), IN nexts VARCHAR(32))
BEGIN
  DECLARE mid INT;
  DECLARE mcnt INT;
  DECLARE cnt INT;
  select markov.id, markov.count,count(*) into mid,mcnt,cnt from markov where markov.now=nows and markov.next=nexts;
  if cnt > 0 then
    update markov set count = mcnt+1 where markov.id = mid;
  else
    insert into markov(now,next,count) VALUES(nows,nexts,1);
  end if;
END
