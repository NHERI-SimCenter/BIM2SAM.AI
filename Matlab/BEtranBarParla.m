function tbar=BEtranBarParla(l,h,t,nl,nh,nt,spacel,spaceh,spacet,diam,p0,matType)

    tbar=[];
    bars=[];
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
    
    z=[];
    if mod(nh,2)==1
        z=[0];
        for i=1:floor(nh/2)
            z=[z,spaceh*i,-spaceh*i];
        end
    else
        for i=1:nh/2
            z=[z,spaceh*i-spaceh/2,-spaceh*i+spaceh/2];
        end
    end
    
    
    
    if nt>1
        for i=1:nl
            c=p0+[x(i), 0, 0];
            box=[diam, spacet*(nt-1),diam];
            bars=[bars;c,box,matType]; 
        end
    end
    
    if nl>1
        for i=1:nt
            c=p0+[0, y(i), 0];
            box=[spacel*(nl-1),diam,diam];
            bars=[bars;c,box,matType];
        end
    end
    
   
    
    
    for i=1:nh
        n=size(bars,1);
        dir=ones(n,1)*([0,0,z(i)+h/2]);
        tempBars=bars;
        tempBars(:,1:3)=tempBars(:,1:3)+dir;
        tbar=[tbar;tempBars]; 
    end
