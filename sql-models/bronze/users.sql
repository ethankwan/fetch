CREATE TABLE bronze.users (
	id text primary key,
	"state" text,
	"createdDate" bigint,
	"role" text,
	"active" boolean,
    "signUpSource" text,
    "lastLoginDate" numeric
);