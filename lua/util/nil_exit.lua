function Nil_to_exit(data, err_log)
    if data == nil or not data then
        ngx.log(ngx.ERR, err_log .. err)
        ngx.exit(ngx.ERROR)
    end
end
