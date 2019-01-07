function lbar=longBarPara(l,h,t,nl,nt,spacel,spacet,diam,p0,matType)
    %lbar=[p0+[0,0,h/2],l,t,h];
    lbar=[];
    x=[];
    if mod(nl,2)==1
        x=[0];
        for i=1:floor(nl/2)
            x=[x,spacel*i,-spacel*i];
        end
    else
        for i=1:nl/2
            x=[x,spacel*i-spacel/2,-spacel*i+spacel/2];
        end
    end
    
    y=[];
    if mod(nt,2)==1
        y=[0];
        for i=1:floor(nt/2)
            y=[y,spacet*i,-spacet*i];
        end
    else
        for i=1:nt/2
            y=[y,spacet*i-spacet/2,-spacet*i+spacet/2];
        end
    end
    
    for i=1:nl
        for j=1:nt
            c=p0+[x(i), y(j), h/2];
            box=[diam, diam, h];
            lbar=[lbar;c,box,matType];           
        end
    end
