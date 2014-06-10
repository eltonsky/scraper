
# CREATE DATABASE IF NOT EXISTS rea;

#use rea;

# taddr
CREATE TABLE IF NOT EXISTS taddr (
  addr_id 	INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  street_no    VARCHAR(16),
  street_name  VARCHAR(64) NOT NULL, # can be "POA","Contact Agent"
  INDEX street_name_ix (street_name),

  locality     VARCHAR(64),
  INDEX locality_ix (locality),

  region       VARCHAR(16),
  INDEX region_ix(region),

  postcode     VARCHAR(4), 
  INDEX postcode_ix(postcode),

  UNIQUE KEY addr_unique_ix (street_no,street_name,locality,region),

  cr_date 	TIMESTAMP DEFAULT NOW()
) ENGINE=INNODB ;


# tagentcy
CREATE TABLE IF NOT EXISTS tagency (
  agency_id   INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  name      VARCHAR(32) NOT NULL,
  cr_date   TIMESTAMP DEFAULT NOW()
) ENGINE=INNODB ;


# tproperty
CREATE TABLE IF NOT EXISTS tproperty (
  prop_id 	INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  ext_id  	INT,
  addr_id 	INT NOT NULL,
  FOREIGN KEY (addr_id) 
        REFERENCES taddr(addr_id),
  type    	VARCHAR(32),
  INDEX type_ix(type),

  land_size VARCHAR(128),
  cr_date 	TIMESTAMP DEFAULT NOW()
) ENGINE=INNODB ;


# tsale
CREATE TABLE IF NOT EXISTS tsale (
  sale_id 	INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  prop_id   INT NOT NULL,
  FOREIGN KEY (prop_id) 
        REFERENCES tproperty(prop_id),

  agency_id INT NOT NULL,
  FOREIGN KEY (agency_id) 
        REFERENCES tagency(agency_id),  

  status    VARCHAR(32) NOT NULL DEFAULT "LISTED",
  INDEX status_ix(status),

  cr_date 	TIMESTAMP DEFAULT NOW()
) ENGINE=INNODB ;


# tprice
CREATE TABLE IF NOT EXISTS tprice (
  price_id   INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  sale_id 	INT NOT NULL,
  FOREIGN KEY (sale_id) 
        REFERENCES tsale(sale_id),
  INDEX sale_id_ix(sale_id),

  price    VARCHAR(32) NOT NULL,
  type     VARCHAR(16),
  INDEX type_ix(type),

  cr_date 	TIMESTAMP DEFAULT NOW()
) ENGINE=INNODB ;


# tfeature
CREATE TABLE IF NOT EXISTS tfeatures (
  sale_id 	INT NOT NULL,
  FOREIGN KEY (sale_id) 
        REFERENCES tsale(sale_id),
  INDEX sale_id_ix(sale_id),

  bed       INT,
  INDEX bed_ix(bed),

  bath      INT,
  INDEX bath_ix(bath),

  car_spaces INT,
  INDEX car_space_ix(car_spaces),

  land_size VARCHAR(128),

  cr_date 	TIMESTAMP DEFAULT NOW()
) ENGINE=INNODB ;


# tsalestatus
CREATE TABLE IF NOT EXISTS tsalestatus (
  sale_id 	INT NOT NULL,
  FOREIGN KEY (sale_id) 
        REFERENCES tsale(sale_id),
  INDEX sale_id_ix(sale_id),

  status    VARCHAR(32) NOT NULL,   

  cr_date 	TIMESTAMP DEFAULT NOW()
) ENGINE=INNODB ;


# tinspection
CREATE TABLE IF NOT EXISTS tinspection (
  inspection_id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
  sale_id 	INT NOT NULL,
  FOREIGN KEY (sale_id) 
        REFERENCES tsale(sale_id),
  INDEX sale_id_ix(sale_id),

  start    VARCHAR(32) NOT NULL,
  end      VARCHAR(32) NOT NULL,

  cr_date 	TIMESTAMP DEFAULT NOW()
) ENGINE=INNODB ;


# tagent
CREATE TABLE IF NOT EXISTS tagent (
  agent_id 	INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  name      VARCHAR(32) NOT NULL,
  phone     VARCHAR(32),
  agency_id INT,
  FOREIGN KEY (agency_id) 
        REFERENCES tagency(agency_id), 

  cr_date 	TIMESTAMP DEFAULT NOW()
) ENGINE=INNODB ;


# tSaleAgent
CREATE TABLE IF NOT EXISTS tsaleagent (
  sale_agent_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  agent_id 	INT NOT NULL,
  FOREIGN KEY (agent_id) 
        REFERENCES tagent(agent_id), 
  INDEX agent_id_ix(agent_id),
  sale_id   INT NOT NULL,
  FOREIGN KEY (sale_id) 
        REFERENCES tsale(sale_id),
  INDEX sale_id_ix(sale_id)
) ENGINE=INNODB ;


