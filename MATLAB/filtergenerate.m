function filt=filtergenerate(handles)
% If transfer function is revolved, filt has two column
% First column is transfer function
% Second column is weighted by spectra
global lambda_min;
global lambda_max;
global lambda_step;
global factor;
global passband1;
global passband2;
global weight_spectra;
global transferfunction;
if get(handles.checkbox5,'Value')~=1 %transfer function
    pm1=mod(passband1,lambda_step);
    pm2=mod(passband2,lambda_step);
    startm=passband1-pm1;
    if pm2~=0, stopm=passband2-pm1+lambda_step;
    else stopm=passband2;
    end
    m=(lambda_max-lambda_min)/lambda_step+1;
    filt=zeros(m,1);
    for lambda=startm:lambda_step:stopm
        l=(lambda-lambda_min)/lambda_step+1;
        filt(l)=factor;
    end
    for lambda=stopm:lambda_step:lambda_max
        l=(lambda-lambda_min)/lambda_step+1;
        filt(l)=-1;
    end
    filt(:,1)=filt.*weight_spectra(:,1);
else
    filt(:,1)=transferfunction(:,1);
    pm1=mod(passband1,lambda_step);
    pm2=mod(passband2,lambda_step);
    startm=passband1-pm1;
    if pm2~=0, stopm=passband2-pm1+lambda_step;
    else stopm=passband2;
    end
    m=(lambda_max-lambda_min)/lambda_step+1;
    filt(:,2)=ones(m,1);
    for lambda=startm:lambda_step:stopm
        l=(lambda-lambda_min)/lambda_step+1;
        filt(l,2)=factor;
    end
    
    filt(:,2)=filt(l,2).*weight_spectra(:,1);
end

