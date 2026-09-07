uvicorn app.run:app --host 0.0.0.0 --port 8080 --ssl-keyfile=key.pem --ssl-certfile=cert.pem


One catch

Because that certificate is self-signed, your phone/browser will say something like:

⚠️ Your connection is not private

That's expected. It doesn't mean the encryption isn't working; it means your phone doesn't trust the certificate'
