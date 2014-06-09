cat whitehorse.ls | awk '
BEGIN {IFS=" "}
{
	printf $(NF)" ";
	for (i=1; i<=NF-1; i++) 
		printf $i" ";
	print"";
} 
'