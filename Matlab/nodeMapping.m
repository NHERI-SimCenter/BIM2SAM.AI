 function m=nodeMapping(w,h,level,pt)
 n=0;
 x=[0,w];
 y=0:h/level:h;
for cline=1:2
    for floor=0:level
        n=n+1;
        m(n).cline=cline;
        m(n).floor=floor;
        p=[x(cline),y(floor+1)];
        dpt=pt-ones(size(pt,1),1)*p;
        s=sum(dpt.*dpt,2);
        node=find(s==min(s));
        m(n).node=node;       
    end
end