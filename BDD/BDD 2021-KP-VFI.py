import sys
#sys.path.append(r"C:\IronPython2.7\Lib")
#import traceback
import datetime
from System import DateTime

exceptionList = []

#Provera da li Forma postoji
def getForme(Zahtev,nazivForme):
    if nazivForme in Zahtev.Forme:
        return Zahtev.Forme[nazivForme].NumerickaPoljaForme
    else:
        raise Exception('Obrazac pod nazivom: '+nazivForme+' ne postoji')


#BROJ KONVERTUJE U AOP KEY
def broj_u_aop(aop_broj, broj_kolone):
    seq = ("aop", str(aop_broj).zfill(4), str(broj_kolone))
    aop_key = "_".join(seq)
    return aop_key

#VRACA VREDNOST AOP POLJA
def aop(aop_dict, aop_broj, kolona):   
    aop_key = broj_u_aop(aop_broj, kolona)

    if aop_key in aop_dict:
        a=aop_dict[aop_key]
       
        if a is None:
            return 0
        return a

    raise Exception('Validacion skripta očekuje ' + aop_key + ' koji nije pronadjen')

    
#SUMA OD, DO ZA ZADATU KLOLONU
def suma(aop_dict, prvi_aop, poslednji_aop, kolona):
    sum = 0
    for x in range (prvi_aop, poslednji_aop+1):
        sum += aop(aop_dict, x, kolona)
    return sum

#SUMA AOPA SA LISTE
def suma_liste(aop_dict, lista, kolona):
    sum = 0
    for x in lista:
        sum += aop(aop_dict, x, kolona)
    return sum 

#LISTA NEGATIVNIH PO OBRASCU
def find_negativni(aop_dict, prvi_aop, poslednji_aop, prva_kolona, poslednja_kolona): 
    aopi = ""
    for aop_broj in range (prvi_aop,poslednji_aop+1):
        for kolona in range (prva_kolona,poslednja_kolona+1):
                aop_key = broj_u_aop(aop_broj, kolona)
                if aop_key in aop_dict:
                    a=aop_dict[aop_key]       
                    if not (a is None):
                        if a < 0 :
                            aopi += "AOP " + str(aop_broj).zfill(4) + " kol. " + str(kolona) + " = " + str(aop(aop_dict, aop_broj, kolona)) + ", "                
    if len(aopi) > 0:
         aopi = aopi.Substring(0,aopi.Length-2)
    return aopi
   

def Validate(Zahtev):
    try:
        doc_errors=[]
        doc_warnings=[]
        form_warnings=[]
        form_errors=[]
        ostalo_warnings = []
        ostalo_errors = []
        exceptions=[]
        
        #Provera da li lice odgovorno za sastavljanje je upisano
        if (Zahtev.LiceOdgovornoZaSastavljanje is None):
            ostalo_errors.append('Podaci za lice odgovorno za sastavljanje finansijskog izveštaja nisu upisani.')

       #Provera da li lice odgovorno za potpisivanje
        if (len(Zahtev.Potpisnici) == 0):
            ostalo_errors.append('Podaci o potpisniku finansijskog izveštaja nisu upisani.')
        
        #Provera da li su prosledjeni svi ulazni dokumenti
        if (Zahtev.ValidacijaUlaznihDokumenataOmoguceno==True):
            if Zahtev.UlazniDokumenti.Count>0:
                for k in Zahtev.UlazniDokumenti.Keys:
                    if Zahtev.UlazniDokumenti[k].Obavezan==True and Zahtev.UlazniDokumenti[k].Barkod == None:
                        doc_errors.append('Dokument sa nazivom "'+Zahtev.UlazniDokumenti[k].Naziv+'" niste priložili.')


        #Prilagoditi proveru postojanja forme u zavisnosti od tipa FI
        bs = getForme(Zahtev,'Bilans stanja')
        if len(bs)==0:
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Bilans stanja nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        bu = getForme(Zahtev,'Bilans uspeha')
        if len(bu)==0:
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Bilans uspeha nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

             
        if len(form_errors)>0:
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

        lzbir = 0
        dzbir = 0
        razlika = 0

        ######################################
        #### POCETAK KONTROLNIH PRAVILA ######
        ######################################

        #00000-1
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-2
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-3
        if not( suma(bs,1,30,5)+suma(bs,1,30,6)+suma(bs,1,30,7)+suma(bs,401,448,5)+suma(bs,401,448,6)+suma(bs,401,448,7)+suma(bu,1001,1038,5)+suma(bu,1001,1038,6) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol.5 + (0001 do 0030) kol.6 + (0001 do 0030) kol.7 bilansa stanja + (0401 do 0448) kol. 5 + (0401 do 0448) kol. 6 + (0401 do 0448) kol. 7 bilansa stanja + (1001 do 1038) kol. 5 + (1001 do 1038) kol. 6 bilansa uspeha > 0 Vanredni finansijski izveštaj, po pravilu ne sme biti bez podataka; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol.5 + (0001 do 0030) kol.6 + (0001 do 0030) kol.7 bilansa stanja + (0401 do 0448) kol. 5 + (0401 do 0448) kol. 6 + (0401 do 0448) kol. 7 bilansa stanja + (1001 do 1038) kol. 5 + (1001 do 1038) kol. 6 bilansa uspeha > 0 Vanredni finansijski izveštaj, po pravilu ne sme biti bez podataka; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #00000-4
        #Za ovaj set se ne primenjuje pravilo

        #Provera da li je fizahtev placen
        if not(Zahtev.Placen):
            ostalo_errors.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');

        #Provera negativnih AOP-a
        lista=""
        lista_bs = find_negativni(bs, 1, 448, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1038, 5, 6)
               
        if (len(lista_bs) > 0):
            lista = lista_bs
        if len(lista_bu) > 0:
            if len(lista) > 0:
                lista = lista + ", " + lista_bu
            else:
                lista = lista_bu                           
        if len(lista) > 0:                                           
            
            naziv_obrasca='Bilans stanja'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ="Unete vrednosti ne mogu biti negativne ! (" + lista + ")"
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
 
        
        #BILANS STANJA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #00001
        if not( suma(bs,1,30,5)+suma(bs,401,448,5) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol. 5 + (0401 do 0448) kol. 5 > 0 Bilans stanja, po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #00002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,30,6)+suma(bs,401,448,6) == 0 ):
                lzbir =  suma(bs,1,30,6)+suma(bs,401,448,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol. 6 + (0401 do 0448) kol. 6 = 0 Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00003
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,30,7)+suma(bs,401,448,7) == 0 ):
                lzbir =  suma(bs,1,30,7)+suma(bs,401,448,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol. 7 + (0401 do 0448) kol. 7 = 0 Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00004
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,30,6)+suma(bs,401,448,6) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol. 6 + (0401 do 0448) kol. 6 > 0 Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00005
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,30,7)+suma(bs,401,448,7) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0030) kol. 7 + (0401 do 0448) kol. 7 > 0 Bilans stanja, po pravilu,  mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00006
        if not( aop(bs,1,5) == suma_liste(bs,[2,3,6,9,10,11,12],5) ):
            lzbir =  aop(bs,1,5) 
            dzbir =  suma_liste(bs,[2,3,6,9,10,11,12],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 5 = AOP-u (0002 + 0003 + 0006 + 0009 + 0010 + 0011 + 0012) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00007
        if not( aop(bs,1,6) == suma_liste(bs,[2,3,6,9,10,11,12],6) ):
            lzbir =  aop(bs,1,6) 
            dzbir =  suma_liste(bs,[2,3,6,9,10,11,12],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 6 = AOP-u (0002 + 0003 + 0006 + 0009 + 0010 + 0011 + 0012) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00008
        if not( aop(bs,1,7) == suma_liste(bs,[2,3,6,9,10,11,12],7) ):
            lzbir =  aop(bs,1,7) 
            dzbir =  suma_liste(bs,[2,3,6,9,10,11,12],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0001 kol. 7 = AOP-u (0002 + 0003 + 0006 + 0009 + 0010 + 0011 + 0012) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00009
        if not( aop(bs,3,5) == suma(bs,4,5,5) ):
            lzbir =  aop(bs,3,5) 
            dzbir =  suma(bs,4,5,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0003 kol. 5 = AOP-u (0004 + 0005) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00010
        if not( aop(bs,3,6) == suma(bs,4,5,6) ):
            lzbir =  aop(bs,3,6) 
            dzbir =  suma(bs,4,5,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0003 kol. 6 = AOP-u (0004 + 0005) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00011
        if not( aop(bs,3,7) == suma(bs,4,5,7) ):
            lzbir =  aop(bs,3,7) 
            dzbir =  suma(bs,4,5,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0003 kol. 7 = AOP-u (0004 + 0005) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00012
        if not( aop(bs,6,5) == suma(bs,7,8,5) ):
            lzbir =  aop(bs,6,5) 
            dzbir =  suma(bs,7,8,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0006 kol. 5 = AOP-u (0007 + 0008) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00013
        if not( aop(bs,6,6) == suma(bs,7,8,6) ):
            lzbir =  aop(bs,6,6) 
            dzbir =  suma(bs,7,8,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0006 kol. 6 = AOP-u (0007 + 0008) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00014
        if not( aop(bs,6,7) == suma(bs,7,8,7) ):
            lzbir =  aop(bs,6,7) 
            dzbir =  suma(bs,7,8,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0006 kol. 7 = AOP-u (0007 + 0008) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00015
        if not( aop(bs,13,5) == suma_liste(bs,[14,15,16,24],5) ):
            lzbir =  aop(bs,13,5) 
            dzbir =  suma_liste(bs,[14,15,16,24],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 5 = AOP-u (0014 + 0015 + 0016 + 0024) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00016
        if not( aop(bs,13,6) == suma_liste(bs,[14,15,16,24],6) ):
            lzbir =  aop(bs,13,6) 
            dzbir =  suma_liste(bs,[14,15,16,24],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 6 = AOP-u (0014 + 0015 + 0016 + 0024) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00017
        if not( aop(bs,13,7) == suma_liste(bs,[14,15,16,24],7) ):
            lzbir =  aop(bs,13,7) 
            dzbir =  suma_liste(bs,[14,15,16,24],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0013 kol. 7 = AOP-u (0014 + 0015 + 0016 + 0024) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00018
        if not( aop(bs,16,5) == suma(bs,17,23,5) ):
            lzbir =  aop(bs,16,5) 
            dzbir =  suma(bs,17,23,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0016 kol. 5 = AOP-u (0017 + 0018 + 0019 + 0020 + 0021 + 0022 + 0023) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00019
        if not( aop(bs,16,6) == suma(bs,17,23,6) ):
            lzbir =  aop(bs,16,6) 
            dzbir =  suma(bs,17,23,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0016 kol. 6 = AOP-u (0017 + 0018 + 0019 + 0020 + 0021 + 0022 + 0023) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00020
        if not( aop(bs,16,7) == suma(bs,17,23,7) ):
            lzbir =  aop(bs,16,7) 
            dzbir =  suma(bs,17,23,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0016 kol. 7 = AOP-u (0017 + 0018 + 0019 + 0020 + 0021 + 0022 + 0023) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00021
        if not( aop(bs,24,5) == suma(bs,25,26,5) ):
            lzbir =  aop(bs,24,5) 
            dzbir =  suma(bs,25,26,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0024 kol. 5 = AOP-u (0025 + 0026) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00022
        if not( aop(bs,24,6) == suma(bs,25,26,6) ):
            lzbir =  aop(bs,24,6) 
            dzbir =  suma(bs,25,26,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0024 kol. 6 = AOP-u (0025 + 0026) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00023
        if not( aop(bs,24,7) == suma(bs,25,26,7) ):
            lzbir =  aop(bs,24,7) 
            dzbir =  suma(bs,25,26,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0024 kol. 7 = AOP-u (0025 + 0026) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00024
        if not( aop(bs,29,5) == suma_liste(bs,[1,13,27,28],5) ):
            lzbir =  aop(bs,29,5) 
            dzbir =  suma_liste(bs,[1,13,27,28],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0029 kol. 5 = AOP-u (0001 + 0013 + 0027 + 0028) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00025
        if not( aop(bs,29,6) == suma_liste(bs,[1,13,27,28],6) ):
            lzbir =  aop(bs,29,6) 
            dzbir =  suma_liste(bs,[1,13,27,28],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0029 kol. 6 = AOP-u (0001 + 0013 + 0027 + 0028) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00026
        if not( aop(bs,29,7) == suma_liste(bs,[1,13,27,28],7) ):
            lzbir =  aop(bs,29,7) 
            dzbir =  suma_liste(bs,[1,13,27,28],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0029 kol. 7 = AOP-u (0001 + 0013 + 0027 + 0028) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00027
        if( suma_liste(bs,[402,404,407,408,409,411,414],5) > suma_liste(bs,[403,410,415,418],5) ):
            if not( aop(bs,401,5) == suma_liste(bs,[402,404,407,408,409,411,414],5)-suma_liste(bs,[403,410,415,418],5) ):
                lzbir =  aop(bs,401,5) 
                dzbir =  suma_liste(bs,[402,404,407,408,409,411,414],5)-suma_liste(bs,[403,410,415,418],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 5 = AOP-u (0402 - 0403 + 0404 + 0407 + 0408 + 0409 - 0410 + 0411 + 0414 - 0415 - 0418) kol. 5, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414)  kol. 5 > AOP-a (0403 + 0410 + 0415 + 0418) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00028
        if( suma_liste(bs,[402,404,407,408,409,411,414],6) > suma_liste(bs,[403,410,415,418],6) ):
            if not( aop(bs,401,6) == suma_liste(bs,[402,404,407,408,409,411,414],6)-suma_liste(bs,[403,410,415,418],6) ):
                lzbir =  aop(bs,401,6) 
                dzbir =  suma_liste(bs,[402,404,407,408,409,411,414],6)-suma_liste(bs,[403,410,415,418],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 6 = AOP-u (0402 - 0403 + 0404 + 0407 + 0408 + 0409 - 0410 + 0411 + 0414 - 0415 - 0418) kol. 6, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414)  kol. 6 > AOP-a (0403 + 0410 + 0415 + 0418) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00029
        if( suma_liste(bs,[402,404,407,408,409,411,414],7) > suma_liste(bs,[403,410,415,418],7) ):
            if not( aop(bs,401,7) == suma_liste(bs,[402,404,407,408,409,411,414],7)-suma_liste(bs,[403,410,415,418],7) ):
                lzbir =  aop(bs,401,7) 
                dzbir =  suma_liste(bs,[402,404,407,408,409,411,414],7)-suma_liste(bs,[403,410,415,418],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 7 = AOP-u (0402 - 0403 + 0404 + 0407 + 0408 + 0409 - 0410 + 0411 + 0414 - 0415 - 0418) kol. 7, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414)  kol. 7 > AOP-a (0403 + 0410 + 0415 + 0418) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00030
        if( aop(bs,29,5) > suma_liste(bs,[419,444,445],5) ):
            if not( aop(bs,401,5) == aop(bs,29,5)-suma_liste(bs,[419,444,445],5) ):
                lzbir =  aop(bs,401,5) 
                dzbir =  aop(bs,29,5)-suma_liste(bs,[419,444,445],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP  0401 kol. 5 = AOP-u (0029 - 0419 - 0444 - 0445) kol. 5, ako je AOP 0029 kol. 5  >  AOP-a (0419 + 0444 + 0445) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00031
        if( aop(bs,29,6) > suma_liste(bs,[419,444,445],6) ):
            if not( aop(bs,401,6) == aop(bs,29,6)-suma_liste(bs,[419,444,445],6) ):
                lzbir =  aop(bs,401,6) 
                dzbir =  aop(bs,29,6)-suma_liste(bs,[419,444,445],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP  0401 kol. 6 = AOP-u (0029 - 0419 - 0444 - 0445) kol. 6, ako je AOP 0029 kol. 6 > AOP-a (0419 + 0444 + 0445) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00032
        if( aop(bs,29,7) > suma_liste(bs,[419,444,445],7) ):
            if not( aop(bs,401,7) == aop(bs,29,7)-suma_liste(bs,[419,444,445],7) ):
                lzbir =  aop(bs,401,7) 
                dzbir =  aop(bs,29,7)-suma_liste(bs,[419,444,445],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP  0401 kol. 7 = AOP-u (0029 - 0419 - 0444 - 0445) kol. 7, ako je AOP 0029 kol. 7 > AOP-a (0419 + 0444 + 0445) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00033
        if not( aop(bs,404,5) == suma(bs,405,406,5) ):
            lzbir =  aop(bs,404,5) 
            dzbir =  suma(bs,405,406,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0404 kol. 5 = AOP-u (0405 + 0406) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00034
        if not( aop(bs,404,6) == suma(bs,405,406,6) ):
            lzbir =  aop(bs,404,6) 
            dzbir =  suma(bs,405,406,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0404 kol. 6 = AOP-u (0405 + 0406) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00035
        if not( aop(bs,404,7) == suma(bs,405,406,7) ):
            lzbir =  aop(bs,404,7) 
            dzbir =  suma(bs,405,406,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0404 kol. 7 = AOP-u (0405 + 0406) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00036
        if not( aop(bs,411,5) == suma(bs,412,413,5) ):
            lzbir =  aop(bs,411,5) 
            dzbir =  suma(bs,412,413,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0411 kol. 5 = AOP-u (0412 + 0413) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00037
        if not( aop(bs,411,6) == suma(bs,412,413,6) ):
            lzbir =  aop(bs,411,6) 
            dzbir =  suma(bs,412,413,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0411 kol. 6 = AOP-u (0412 + 0413) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00038
        if not( aop(bs,411,7) == suma(bs,412,413,7) ):
            lzbir =  aop(bs,411,7) 
            dzbir =  suma(bs,412,413,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0411 kol. 7 = AOP-u (0412 + 0413) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00039
        if not( aop(bs,414,5) == 0 ):
            lzbir =  aop(bs,414,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0414 kol. 5 = 0 Učešće bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00040
        if not( aop(bs,414,6) == 0 ):
            lzbir =  aop(bs,414,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0414 kol. 6 = 0 Učešće bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00041
        if not( aop(bs,414,7) == 0 ):
            lzbir =  aop(bs,414,7) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0414 kol. 7 = 0 Učešće bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00042
        if not( aop(bs,415,5) == suma(bs,416,417,5) ):
            lzbir =  aop(bs,415,5) 
            dzbir =  suma(bs,416,417,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0415 kol. 5 = AOP-u (0416 + 0417) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00043
        if not( aop(bs,415,6) == suma(bs,416,417,6) ):
            lzbir =  aop(bs,415,6) 
            dzbir =  suma(bs,416,417,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0415 kol. 6 = AOP-u (0416 + 0417) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00044
        if not( aop(bs,415,7) == suma(bs,416,417,7) ):
            lzbir =  aop(bs,415,7) 
            dzbir =  suma(bs,416,417,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0415 kol. 7 = AOP-u (0416 + 0417) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00045
        if not( aop(bs,419,5) == suma_liste(bs,[420,421,422,428,434,440],5) ):
            lzbir =  aop(bs,419,5) 
            dzbir =  suma_liste(bs,[420,421,422,428,434,440],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0419 kol. 5 = AOP-u (0420 + 0421 + 0422 + 0428 + 0434 + 0440) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00046
        if not( aop(bs,419,6) == suma_liste(bs,[420,421,422,428,434,440],6) ):
            lzbir =  aop(bs,419,6) 
            dzbir =  suma_liste(bs,[420,421,422,428,434,440],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0419 kol. 6 = AOP-u (0420 + 0421 + 0422 + 0428 + 0434 + 0440) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00047
        if not( aop(bs,419,7) == suma_liste(bs,[420,421,422,428,434,440],7) ):
            lzbir =  aop(bs,419,7) 
            dzbir =  suma_liste(bs,[420,421,422,428,434,440],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0419 kol. 7 = AOP-u (0420 + 0421 + 0422 + 0428 + 0434 + 0440) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00048
        if not( aop(bs,422,5) == suma(bs,423,427,5) ):
            lzbir =  aop(bs,422,5) 
            dzbir =  suma(bs,423,427,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0422 kol. 5 = AOP-u (0423 + 0424 + 0425 + 0426 + 0427) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00049
        if not( aop(bs,422,6) == suma(bs,423,427,6) ):
            lzbir =  aop(bs,422,6) 
            dzbir =  suma(bs,423,427,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0422 kol. 6 = AOP-u (0423 + 0424 + 0425 + 0426 + 0427) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00050
        if not( aop(bs,422,7) == suma(bs,423,427,7) ):
            lzbir =  aop(bs,422,7) 
            dzbir =  suma(bs,423,427,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0422 kol. 7 = AOP-u (0423 + 0424 + 0425 + 0426 + 0427) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00051
        if not( aop(bs,428,5) == suma(bs,429,433,5) ):
            lzbir =  aop(bs,428,5) 
            dzbir =  suma(bs,429,433,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0428 kol. 5 = AOP-u (0429 + 0430 + 0431 + 0432 + 0433) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00052
        if not( aop(bs,428,6) == suma(bs,429,433,6) ):
            lzbir =  aop(bs,428,6) 
            dzbir =  suma(bs,429,433,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0428 kol. 6 = AOP-u (0429 + 0430 + 0431 + 0432 + 0433) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00053
        if not( aop(bs,428,7) == suma(bs,429,433,7) ):
            lzbir =  aop(bs,428,7) 
            dzbir =  suma(bs,429,433,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0428 kol. 7 = AOP-u (0429 + 0430 + 0431 + 0432 + 0433) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00054
        if not( aop(bs,434,5) == suma(bs,435,439,5) ):
            lzbir =  aop(bs,434,5) 
            dzbir =  suma(bs,435,439,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0434 kol. 5 = AOP-u (0435 + 0436 + 0437 + 0438 + 0439) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00055
        if not( aop(bs,434,6) == suma(bs,435,439,6) ):
            lzbir =  aop(bs,434,6) 
            dzbir =  suma(bs,435,439,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0434 kol. 6 = AOP-u (0435 + 0436 + 0437 + 0438 + 0439) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00056
        if not( aop(bs,434,7) == suma(bs,435,439,7) ):
            lzbir =  aop(bs,434,7) 
            dzbir =  suma(bs,435,439,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0434 kol. 7 = AOP-u (0435 + 0436 + 0437 + 0438 + 0439) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00057
        if not( aop(bs,440,5) == suma(bs,441,443,5) ):
            lzbir =  aop(bs,440,5) 
            dzbir =  suma(bs,441,443,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0440 kol. 5 = AOP-u (0441 + 0442 + 0443) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00058
        if not( aop(bs,440,6) == suma(bs,441,443,6) ):
            lzbir =  aop(bs,440,6) 
            dzbir =  suma(bs,441,443,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0440 kol. 6 = AOP-u (0441 + 0442 + 0443) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00059
        if not( aop(bs,440,7) == suma(bs,441,443,7) ):
            lzbir =  aop(bs,440,7) 
            dzbir =  suma(bs,441,443,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0440 kol. 7 = AOP-u (0441 + 0442 + 0443) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00060
        if( suma_liste(bs,[402,404,407,408,409,411,414],5) < suma_liste(bs,[403,410,415,418],5) ):
            if not( aop(bs,446,5) == suma_liste(bs,[403,410,415,418],5)-suma_liste(bs,[402,404,407,408,409,411,414],5) ):
                lzbir =  aop(bs,446,5) 
                dzbir =  suma_liste(bs,[403,410,415,418],5)-suma_liste(bs,[402,404,407,408,409,411,414],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0446 kol. 5 = AOP-u (0403 + 0410 + 0415 + 0418 - 0402 - 0404 - 0407 - 0408 - 0409 - 0411 - 0414) kol. 5, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414) kol. 5 < AOP-a (0403 + 0410 + 0415 + 0418) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00061
        if( suma_liste(bs,[402,404,407,408,409,411,414],6) < suma_liste(bs,[403,410,415,418],6) ):
            if not( aop(bs,446,6) == suma_liste(bs,[403,410,415,418],6)-suma_liste(bs,[402,404,407,408,409,411,414],6) ):
                lzbir =  aop(bs,446,6) 
                dzbir =  suma_liste(bs,[403,410,415,418],6)-suma_liste(bs,[402,404,407,408,409,411,414],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0446 kol. 6 = AOP-u (0403 + 0410 + 0415 + 0418 - 0402 - 0404 - 0407 - 0408 - 0409 - 0411 - 0414) kol. 6, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414) kol. 6 < AOP-a (0403 + 0410 + 0415 + 0418) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00062
        if( suma_liste(bs,[402,404,407,408,409,411,414],7) < suma_liste(bs,[403,410,415,418],7) ):
            if not( aop(bs,446,7) == suma_liste(bs,[403,410,415,418],7)-suma_liste(bs,[402,404,407,408,409,411,414],7) ):
                lzbir =  aop(bs,446,7) 
                dzbir =  suma_liste(bs,[403,410,415,418],7)-suma_liste(bs,[402,404,407,408,409,411,414],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0446 kol. 7 = AOP-u (0403 + 0410 + 0415 + 0418 - 0402 - 0404 - 0407 - 0408 - 0409 - 0411 - 0414) kol. 7, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414) kol. 7 < AOP-a (0403 + 0410 + 0415 + 0418) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00063
        if( aop(bs,29,5) < suma_liste(bs,[419,444,445],5) ):
            if not( aop(bs,446,5) == suma_liste(bs,[419,444,445],5)-aop(bs,29,5) ):
                lzbir =  aop(bs,446,5) 
                dzbir =  suma_liste(bs,[419,444,445],5)-aop(bs,29,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0446 kol. 5 = AOP-u (0419 + 0444 + 0445 - 0029) kol. 5, ako je AOP 0029 kol. 5 < AOP-a (0419 + 0444 + 0445) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00064
        if( aop(bs,29,6) < suma_liste(bs,[419,444,445],6) ):
            if not( aop(bs,446,6) == suma_liste(bs,[419,444,445],6)-aop(bs,29,6) ):
                lzbir =  aop(bs,446,6) 
                dzbir =  suma_liste(bs,[419,444,445],6)-aop(bs,29,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0446 kol. 6 = AOP-u (0419 + 0444 + 0445 - 0029) kol. 6, ako je AOP 0029 kol. 6 < AOP-a (0419 + 0444 + 0445) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00065
        if( aop(bs,29,7) < suma_liste(bs,[419,444,445],7) ):
            if not( aop(bs,446,7) == suma_liste(bs,[419,444,445],7)-aop(bs,29,7) ):
                lzbir =  aop(bs,446,7) 
                dzbir =  suma_liste(bs,[419,444,445],7)-aop(bs,29,7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0446 kol. 7 = AOP-u (0419 + 0444 + 0445 - 0029) kol. 7, ako je AOP 0029 kol. 7 < AOP-a (0419 + 0444 + 0445) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00066
        if( suma_liste(bs,[402,404,407,408,409,411,414],5) == suma_liste(bs,[403,410,415,418],5) ):
            if not( suma_liste(bs,[401,446],5) == 0 ):
                lzbir =  suma_liste(bs,[401,446],5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0446) kol. 5 = 0, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414) kol. 5 = AOP-u (0403 + 0410 + 0415 + 0418) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00067
        if( suma_liste(bs,[402,404,407,408,409,411,414],6) == suma_liste(bs,[403,410,415,418],6) ):
            if not( suma_liste(bs,[401,446],6) == 0 ):
                lzbir =  suma_liste(bs,[401,446],6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0446) kol. 6 = 0, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414) kol. 6 = AOP-u (0403 + 0410 + 0415 + 0418) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00068
        if( suma_liste(bs,[402,404,407,408,409,411,414],7) == suma_liste(bs,[403,410,415,418],7) ):
            if not( suma_liste(bs,[401,446],7) == 0 ):
                lzbir =  suma_liste(bs,[401,446],7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0446) kol. 7 = 0, ako je AOP (0402 + 0404 + 0407 + 0408 + 0409 + 0411 + 0414) kol. 7 = AOP-u (0403 + 0410 + 0415 + 0418) kol. 7 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00069
        if( aop(bs,29,5) == suma_liste(bs,[419,444,445],5) ):
            if not( suma_liste(bs,[401,446],5) == 0 ):
                lzbir =  suma_liste(bs,[401,446],5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0446) kol. 5 = 0, ako je AOP 0029 kol. 5 = AOP-u (0419 + 0444 + 0445) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00070
        if( aop(bs,29,6) == suma_liste(bs,[419,444,445],6) ):
            if not( suma_liste(bs,[401,446],6) == 0 ):
                lzbir =  suma_liste(bs,[401,446],6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0446) kol. 6 = 0, ako je AOP 0029 kol. 6 = AOP-u (0419 + 0444 + 0445) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00071
        if( aop(bs,29,7) == suma_liste(bs,[419,444,445],7) ):
            if not( suma_liste(bs,[401,446],7) == 0 ):
                lzbir =  suma_liste(bs,[401,446],7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0446) kol. 7 = 0, ako je AOP 0029 kol. 7 = AOP-u (0419 + 0444 + 0445) kol. 7 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00072
        if( aop(bs,401,5) > 0 ):
            if not( aop(bs,446,5) == 0 ):
                lzbir =  aop(bs,446,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 5 > 0 onda je AOP 0446 kol. 5 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00073
        if( aop(bs,446,5) > 0 ):
            if not( aop(bs,401,5) == 0 ):
                lzbir =  aop(bs,401,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0446 kol. 5 > 0 onda je AOP 0401 kol. 5 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00074
        if( aop(bs,401,6) > 0 ):
            if not( aop(bs,446,6) == 0 ):
                lzbir =  aop(bs,446,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 6 > 0 onda je AOP 0446 kol. 6 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00075
        if( aop(bs,446,6) > 0 ):
            if not( aop(bs,401,6) == 0 ):
                lzbir =  aop(bs,401,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0446 kol. 6 > 0 onda je AOP 0401 kol. 6 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00076
        if( aop(bs,401,7) > 0 ):
            if not( aop(bs,446,7) == 0 ):
                lzbir =  aop(bs,446,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 7 > 0 onda je AOP 0446 kol. 7 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00077
        if( aop(bs,446,7) > 0 ):
            if not( aop(bs,401,7) == 0 ):
                lzbir =  aop(bs,401,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0446 kol. 7 > 0 onda je AOP 0401 kol. 7 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00078
        if not( aop(bs,447,5) == suma_liste(bs,[401,419,444,445],5)-aop(bs,446,5) ):
            lzbir =  aop(bs,447,5) 
            dzbir =  suma_liste(bs,[401,419,444,445],5)-aop(bs,446,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0447 kol. 5 = AOP-u (0401 + 0419 + 0444 + 0445 - 0446) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00079
        if not( aop(bs,447,6) == suma_liste(bs,[401,419,444,445],6)-aop(bs,446,6) ):
            lzbir =  aop(bs,447,6) 
            dzbir =  suma_liste(bs,[401,419,444,445],6)-aop(bs,446,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0447 kol. 6 = AOP-u (0401 + 0419 + 0444 + 0445 - 0446) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00080
        if not( aop(bs,447,7) == suma_liste(bs,[401,419,444,445],7)-aop(bs,446,7) ):
            lzbir =  aop(bs,447,7) 
            dzbir =  suma_liste(bs,[401,419,444,445],7)-aop(bs,446,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0447 kol. 7 = AOP-u (0401 + 0419 + 0444 + 0445 - 0446) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00081
        if not( aop(bs,29,5) == aop(bs,447,5) ):
            lzbir =  aop(bs,29,5) 
            dzbir =  aop(bs,447,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0029 kol. 5 = AOP-u 0447 kol. 5 Kontrolni pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00082
        if not( aop(bs,29,6) == aop(bs,447,6) ):
            lzbir =  aop(bs,29,6) 
            dzbir =  aop(bs,447,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0029 kol. 6 = AOP-u 0447 kol. 6 Kontrolni pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00083
        if not( aop(bs,29,7) == aop(bs,447,7) ):
            lzbir =  aop(bs,29,7) 
            dzbir =  aop(bs,447,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0029 kol. 7 = AOP-u 0447 kol. 7 Kontrolni pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00084
        if not( aop(bs,30,5) == aop(bs,448,5) ):
            lzbir =  aop(bs,30,5) 
            dzbir =  aop(bs,448,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0030 kol. 5 = AOP-u 0448 kol. 5 Kontrolni pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00085
        if not( aop(bs,30,6) == aop(bs,448,6) ):
            lzbir =  aop(bs,30,6) 
            dzbir =  aop(bs,448,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0030 kol. 6 = AOP-u 0448 kol. 6 Kontrolni pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00086
        if not( aop(bs,30,7) == aop(bs,448,7) ):
            lzbir =  aop(bs,30,7) 
            dzbir =  aop(bs,448,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0030 kol. 7 = AOP-u 0448 kol. 7 Kontrolni pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00087
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if( suma(bu,1001,1038,5) > 0 ):
                if not( suma(bs,1,30,5)+suma(bs,401,448,5) != suma(bs,1,30,6)+suma(bs,401,448,6) ):
                    
                    naziv_obrasca='Bilans uspeha'
                    poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1038) kol. 5 bilansa uspeha > 0 onda zbir podataka na oznakama za AOP (0001 do 0030) kol. 5 + (0401 do 0448) kol. 5 ≠ zbiru podataka na oznakama za AOP (0001 do 0030) kol. 6 + (0401 do 0448) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa stanja su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
                    naziv_obrasca='Bilans stanja'
                    poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1038) kol. 5 bilansa uspeha > 0 onda zbir podataka na oznakama za AOP (0001 do 0030) kol. 5 + (0401 do 0448) kol. 5 ≠ zbiru podataka na oznakama za AOP (0001 do 0030) kol. 6 + (0401 do 0448) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa stanja su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
        
        #BILANS USPEHA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #10001
        if not( suma(bu,1001,1038,5) > 0 ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (1001 do 1038) kol. 5 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #10002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bu,1001,1038,6) == 0 ):
                lzbir =  suma(bu,1001,1038,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1038) kol. 6 = 0 Bilans uspeha za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bu,1001,1038,6) > 0 ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1038) kol. 6 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10004
        if not( aop(bu,1002,5) == suma(bu,1003,1005,5) ):
            lzbir =  aop(bu,1002,5) 
            dzbir =  suma(bu,1003,1005,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1002 kol. 5 = AOP-u (1003 + 1004 + 1005) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10005
        if not( aop(bu,1002,6) == suma(bu,1003,1005,6) ):
            lzbir =  aop(bu,1002,6) 
            dzbir =  suma(bu,1003,1005,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1002 kol. 6 = AOP-u (1003 + 1004 + 1005) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10006
        if( aop(bu,1001,5) > aop(bu,1002,5) ):
            if not( aop(bu,1006,5) == aop(bu,1001,5)-aop(bu,1002,5) ):
                lzbir =  aop(bu,1006,5) 
                dzbir =  aop(bu,1001,5)-aop(bu,1002,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1006 kol. 5 = AOP-u (1001 - 1002) kol. 5, ako je AOP 1001 kol. 5 > AOP-a 1002 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10007
        if( aop(bu,1001,6) > aop(bu,1002,6) ):
            if not( aop(bu,1006,6) == aop(bu,1001,6)-aop(bu,1002,6) ):
                lzbir =  aop(bu,1006,6) 
                dzbir =  aop(bu,1001,6)-aop(bu,1002,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1006 kol. 6 = AOP-u (1001 - 1002) kol. 6, ako je AOP 1001 kol. 6 > AOP-a 1002 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10008
        if( aop(bu,1001,5) < aop(bu,1002,5) ):
            if not( aop(bu,1007,5) == aop(bu,1002,5)-aop(bu,1001,5) ):
                lzbir =  aop(bu,1007,5) 
                dzbir =  aop(bu,1002,5)-aop(bu,1001,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1007 kol. 5 = AOP-u (1002 - 1001) kol. 5, ako je AOP 1001 kol. 5 < AOP-a 1002 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10009
        if( aop(bu,1001,6) < aop(bu,1002,6) ):
            if not( aop(bu,1007,6) == aop(bu,1002,6)-aop(bu,1001,6) ):
                lzbir =  aop(bu,1007,6) 
                dzbir =  aop(bu,1002,6)-aop(bu,1001,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1007 kol. 6 = AOP-u (1002 - 1001) kol. 6, ako je AOP 1001 kol. 6 < AOP-a 1002 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10010
        if( aop(bu,1001,5) == aop(bu,1002,5) ):
            if not( suma(bu,1006,1007,5) == 0 ):
                lzbir =  suma(bu,1006,1007,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  =' AOP (1006 + 1007) kol. 5 = 0, ako je AOP 1001 kol. 5 = AOP-u 1002 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10011
        if( aop(bu,1001,6) == aop(bu,1002,6) ):
            if not( suma(bu,1006,1007,6) == 0 ):
                lzbir =  suma(bu,1006,1007,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  =' AOP (1006 + 1007) kol. 6 = 0, ako je AOP 1001 kol. 6 = AOP-u 1002 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10012
        if( aop(bu,1006,5) > 0 ):
            if not( aop(bu,1007,5) == 0 ):
                lzbir =  aop(bu,1007,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1006 kol. 5 > 0 onda je AOP 1007 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10013
        if( aop(bu,1007,5) > 0 ):
            if not( aop(bu,1006,5) == 0 ):
                lzbir =  aop(bu,1006,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1007 kol. 5 > 0 onda je AOP 1006 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10014
        if( aop(bu,1006,6) > 0 ):
            if not( aop(bu,1007,6) == 0 ):
                lzbir =  aop(bu,1007,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1006 kol. 6 > 0 onda je AOP 1007 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10015
        if( aop(bu,1007,6) > 0 ):
            if not( aop(bu,1006,6) == 0 ):
                lzbir =  aop(bu,1006,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1007 kol. 6 > 0 onda je AOP 1006 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10016
        if not( suma_liste(bu,[1001,1007],5) == suma_liste(bu,[1002,1006],5) ):
            lzbir =  suma_liste(bu,[1001,1007],5) 
            dzbir =  suma_liste(bu,[1002,1006],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1007) kol. 5 = AOP-u (1002 + 1006) kol.5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10017
        if not( suma_liste(bu,[1001,1007],6) == suma_liste(bu,[1002,1006],6) ):
            lzbir =  suma_liste(bu,[1001,1007],6) 
            dzbir =  suma_liste(bu,[1002,1006],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1007) kol. 6 = AOP-u (1002 + 1006) kol.6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10018
        if( aop(bu,1008,5) > aop(bu,1009,5) ):
            if not( aop(bu,1010,5) == aop(bu,1008,5)-aop(bu,1009,5) ):
                lzbir =  aop(bu,1010,5) 
                dzbir =  aop(bu,1008,5)-aop(bu,1009,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1010 kol. 5 = AOP-u (1008 - 1009) kol. 5, ako je AOP 1008 kol. 5 > AOP-a 1009 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10019
        if( aop(bu,1008,6) > aop(bu,1009,6) ):
            if not( aop(bu,1010,6) == aop(bu,1008,6)-aop(bu,1009,6) ):
                lzbir =  aop(bu,1010,6) 
                dzbir =  aop(bu,1008,6)-aop(bu,1009,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1010 kol. 6 = AOP-u (1008 - 1009) kol. 6, ako je AOP 1008 kol. 6 > AOP-a 1009 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10020
        if( aop(bu,1008,5) < aop(bu,1009,5) ):
            if not( aop(bu,1011,5) == aop(bu,1009,5)-aop(bu,1008,5) ):
                lzbir =  aop(bu,1011,5) 
                dzbir =  aop(bu,1009,5)-aop(bu,1008,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1011 kol. 5 = AOP-u (1009 - 1008) kol. 5, ako je AOP 1008 kol. 5 < AOP-a 1009 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10021
        if( aop(bu,1008,6) < aop(bu,1009,6) ):
            if not( aop(bu,1011,6) == aop(bu,1009,6)-aop(bu,1008,6) ):
                lzbir =  aop(bu,1011,6) 
                dzbir =  aop(bu,1009,6)-aop(bu,1008,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1011 kol. 6 = AOP-u (1009 - 1008) kol. 6, ako je AOP 1008 kol. 6 < AOP-a 1009 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10022
        if( aop(bu,1008,5) == aop(bu,1009,5) ):
            if not( suma(bu,1010,1011,5) == 0 ):
                lzbir =  suma(bu,1010,1011,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  =' AOP (1010 + 1011) kol. 5 = 0, ako je AOP 1008 kol. 5 = AOP-u 1009 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10023
        if( aop(bu,1008,6) == aop(bu,1009,6) ):
            if not( suma(bu,1010,1011,6) == 0 ):
                lzbir =  suma(bu,1010,1011,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  =' AOP (1010 + 1011) kol. 6 = 0, ako je AOP 1008 kol. 6 = AOP-u 1009 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10024
        if( aop(bu,1010,5) > 0 ):
            if not( aop(bu,1011,5) == 0 ):
                lzbir =  aop(bu,1011,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1010 kol. 5 > 0 onda je AOP 1011 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10025
        if( aop(bu,1011,5) > 0 ):
            if not( aop(bu,1010,5) == 0 ):
                lzbir =  aop(bu,1010,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1011 kol. 5 > 0 onda je AOP 1010 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10026
        if( aop(bu,1010,6) > 0 ):
            if not( aop(bu,1011,6) == 0 ):
                lzbir =  aop(bu,1011,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1010 kol. 6 > 0 onda je AOP 1011 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10027
        if( aop(bu,1011,6) > 0 ):
            if not( aop(bu,1010,6) == 0 ):
                lzbir =  aop(bu,1010,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1011 kol. 6 > 0 onda je AOP 1010 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10028
        if not( suma_liste(bu,[1008,1011],5) == suma(bu,1009,1010,5) ):
            lzbir =  suma_liste(bu,[1008,1011],5) 
            dzbir =  suma(bu,1009,1010,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1008 + 1011) kol. 5 = AOP-u (1009 + 1010) kol.5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10029
        if not( suma_liste(bu,[1008,1011],6) == suma(bu,1009,1010,6) ):
            lzbir =  suma_liste(bu,[1008,1011],6) 
            dzbir =  suma(bu,1009,1010,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1008 + 1011) kol. 6 = AOP-u (1009 + 1010) kol.6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10030
        if( aop(bu,1012,5) > aop(bu,1013,5) ):
            if not( aop(bu,1014,5) == aop(bu,1012,5)-aop(bu,1013,5) ):
                lzbir =  aop(bu,1014,5) 
                dzbir =  aop(bu,1012,5)-aop(bu,1013,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1014 kol. 5 = AOP-u (1012 - 1013) kol. 5, ako je AOP 1012 kol. 5 > AOP-a 1013 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10031
        if( aop(bu,1012,6) > aop(bu,1013,6) ):
            if not( aop(bu,1014,6) == aop(bu,1012,6)-aop(bu,1013,6) ):
                lzbir =  aop(bu,1014,6) 
                dzbir =  aop(bu,1012,6)-aop(bu,1013,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1014 kol. 6 = AOP-u (1012 - 1013) kol. 6, ako je AOP 1012 kol. 6 > AOP-a 1013 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10032
        if( aop(bu,1012,5) < aop(bu,1013,5) ):
            if not( aop(bu,1015,5) == aop(bu,1013,5)-aop(bu,1012,5) ):
                lzbir =  aop(bu,1015,5) 
                dzbir =  aop(bu,1013,5)-aop(bu,1012,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1015 kol. 5 = AOP-u (1013 - 1012) kol. 5, ako je AOP 1012 kol. 5 < AOP-a 1013 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10033
        if( aop(bu,1012,6) < aop(bu,1013,6) ):
            if not( aop(bu,1015,6) == aop(bu,1013,6)-aop(bu,1012,6) ):
                lzbir =  aop(bu,1015,6) 
                dzbir =  aop(bu,1013,6)-aop(bu,1012,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1015 kol. 6 = AOP-u (1013 - 1012) kol. 6, ako je AOP 1012 kol. 6 < AOP-a 1013 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10034
        if( aop(bu,1012,5) == aop(bu,1013,5) ):
            if not( suma(bu,1014,1015,5) == 0 ):
                lzbir =  suma(bu,1014,1015,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  =' AOP (1014 + 1015) kol. 5 = 0, ako je AOP 1012 kol. 5 = AOP-u 1013 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10035
        if( aop(bu,1012,6) == aop(bu,1013,6) ):
            if not( suma(bu,1014,1015,6) == 0 ):
                lzbir =  suma(bu,1014,1015,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  =' AOP (1014 + 1015) kol. 6 = 0, ako je AOP 1012 kol. 6 = AOP-u 1013 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10036
        if( aop(bu,1014,5) > 0 ):
            if not( aop(bu,1015,5) == 0 ):
                lzbir =  aop(bu,1015,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1014 kol. 5 > 0 onda je AOP 1015 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10037
        if( aop(bu,1015,5) > 0 ):
            if not( aop(bu,1014,5) == 0 ):
                lzbir =  aop(bu,1014,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1015 kol. 5 > 0 onda je AOP 1014 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10038
        if( aop(bu,1014,6) > 0 ):
            if not( aop(bu,1015,6) == 0 ):
                lzbir =  aop(bu,1015,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1014 kol. 6 > 0 onda je AOP 1015 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10039
        if( aop(bu,1015,6) > 0 ):
            if not( aop(bu,1014,6) == 0 ):
                lzbir =  aop(bu,1014,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1015 kol. 6 > 0 onda je AOP 1014 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10040
        if not( suma_liste(bu,[1012,1015],5) == suma(bu,1013,1014,5) ):
            lzbir =  suma_liste(bu,[1012,1015],5) 
            dzbir =  suma(bu,1013,1014,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1012 + 1015) kol. 5 = AOP-u (1013 + 1014) kol.5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10041
        if not( suma_liste(bu,[1012,1015],6) == suma(bu,1013,1014,6) ):
            lzbir =  suma_liste(bu,[1012,1015],6) 
            dzbir =  suma(bu,1013,1014,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1012 + 1015) kol. 6 = AOP-u (1013 + 1014) kol.6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10042
        if not( aop(bu,1016,5) == suma_liste(bu,[1006,1010,1014],5) ):
            lzbir =  aop(bu,1016,5) 
            dzbir =  suma_liste(bu,[1006,1010,1014],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1016 kol. 5 = AOP-u (1006 + 1010 + 1014) kol.5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10043
        if not( aop(bu,1016,6) == suma_liste(bu,[1006,1010,1014],6) ):
            lzbir =  aop(bu,1016,6) 
            dzbir =  suma_liste(bu,[1006,1010,1014],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1016 kol. 6 = AOP-u (1006 + 1010 + 1014) kol.6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10044
        if not( aop(bu,1017,5) == suma_liste(bu,[1007,1011,1015],5) ):
            lzbir =  aop(bu,1017,5) 
            dzbir =  suma_liste(bu,[1007,1011,1015],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1017 kol. 5 = AOP-u (1007 + 1011 + 1015) kol.5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10045
        if not( aop(bu,1017,6) == suma_liste(bu,[1007,1011,1015],6) ):
            lzbir =  aop(bu,1017,6) 
            dzbir =  suma_liste(bu,[1007,1011,1015],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1017 kol. 6 = AOP-u (1007 + 1011 + 1015) kol.6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10046
        if( suma_liste(bu,[1016,1018,1020,1022,1024],5) > suma_liste(bu,[1017,1019,1021,1023,1025],5) ):
            if not( aop(bu,1026,5) == suma_liste(bu,[1016,1018,1020,1022,1024],5)-suma_liste(bu,[1017,1019,1021,1023,1025],5) ):
                lzbir =  aop(bu,1026,5) 
                dzbir =  suma_liste(bu,[1016,1018,1020,1022,1024],5)-suma_liste(bu,[1017,1019,1021,1023,1025],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1026 kol. 5 = AOP-u (1016 - 1017 + 1018 - 1019 + 1020 - 1021 + 1022 - 1023 + 1024 - 1025) kol. 5, ako je AOP (1016 + 1018 + 1020 + 1022 + 1024) kol. 5 > AOP-a (1017 + 1019 + 1021 + 1023 + 1025) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10047
        if( suma_liste(bu,[1016,1018,1020,1022,1024],6) > suma_liste(bu,[1017,1019,1021,1023,1025],6) ):
            if not( aop(bu,1026,6) == suma_liste(bu,[1016,1018,1020,1022,1024],6)-suma_liste(bu,[1017,1019,1021,1023,1025],6) ):
                lzbir =  aop(bu,1026,6) 
                dzbir =  suma_liste(bu,[1016,1018,1020,1022,1024],6)-suma_liste(bu,[1017,1019,1021,1023,1025],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1026 kol. 6 = AOP-u (1016 - 1017 + 1018 - 1019 + 1020 - 1021 + 1022 - 1023 + 1024 - 1025) kol. 6, ako je AOP (1016 + 1018 + 1020 + 1022 + 1024) kol. 6 > AOP-a (1017 + 1019 + 1021 + 1023 + 1025) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10048
        if( suma_liste(bu,[1016,1018,1020,1022,1024],5) < suma_liste(bu,[1017,1019,1021,1023,1025],5) ):
            if not( aop(bu,1027,5) == suma_liste(bu,[1017,1019,1021,1023,1025],5)-suma_liste(bu,[1016,1018,1020,1022,1024],5) ):
                lzbir =  aop(bu,1027,5) 
                dzbir =  suma_liste(bu,[1017,1019,1021,1023,1025],5)-suma_liste(bu,[1016,1018,1020,1022,1024],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1027 kol. 5 = AOP-u (1017 - 1016 + 1019 - 1018 + 1021 - 1020 + 1023 - 1022 + 1025 - 1024) kol. 5, ako je AOP (1016 + 1018 + 1020 + 1022 + 1024) kol. 5 < AOP-a (1017 + 1019 + 1021 + 1023 + 1025) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10049
        if( suma_liste(bu,[1016,1018,1020,1022,1024],6) < suma_liste(bu,[1017,1019,1021,1023,1025],6) ):
            if not( aop(bu,1027,6) == suma_liste(bu,[1017,1019,1021,1023,1025],6)-suma_liste(bu,[1016,1018,1020,1022,1024],6) ):
                lzbir =  aop(bu,1027,6) 
                dzbir =  suma_liste(bu,[1017,1019,1021,1023,1025],6)-suma_liste(bu,[1016,1018,1020,1022,1024],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1027 kol. 6 = AOP-u (1017 - 1016 + 1019 - 1018 + 1021 - 1020 + 1023 - 1022 + 1025 - 1024) kol. 6, ako je AOP (1016 + 1018 + 1020 + 1022 + 1024) kol. 6 < AOP-a (1017 + 1019 + 1021 + 1023 + 1025) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10050
        if( suma_liste(bu,[1016,1018,1020,1022,1024],5) == suma_liste(bu,[1017,1019,1021,1023,1025],5) ):
            if not( suma(bu,1026,1027,5) == 0 ):
                lzbir =  suma(bu,1026,1027,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1026 + 1027) kol. 5 = 0, ako je AOP (1016 + 1018 + 1020 + 1022 + 1024) kol. 5 = AOP-u (1017 + 1019 + 1021 + 1023 + 1025) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10051
        if( suma_liste(bu,[1016,1018,1020,1022,1024],6) == suma_liste(bu,[1017,1019,1021,1023,1025],6) ):
            if not( suma(bu,1026,1027,6) == 0 ):
                lzbir =  suma(bu,1026,1027,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1026 + 1027) kol. 6 = 0, ako je AOP (1016 + 1018 + 1020 + 1022 + 1024) kol. 6 = AOP-u (1017 + 1019 + 1021 + 1023 + 1025) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10052
        if( aop(bu,1026,5) > 0 ):
            if not( aop(bu,1027,5) == 0 ):
                lzbir =  aop(bu,1027,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1026 kol. 5 > 0 onda je AOP 1027 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10053
        if( aop(bu,1027,5) > 0 ):
            if not( aop(bu,1026,5) == 0 ):
                lzbir =  aop(bu,1026,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1027 kol. 5 > 0 onda je AOP 1026 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10054
        if( aop(bu,1026,6) > 0 ):
            if not( aop(bu,1027,6) == 0 ):
                lzbir =  aop(bu,1027,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1026 kol. 6 > 0 onda je AOP 1027 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10055
        if( aop(bu,1027,6) > 0 ):
            if not( aop(bu,1026,6) == 0 ):
                lzbir =  aop(bu,1026,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1027 kol. 6 > 0 onda je AOP 1026 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10056
        if not( suma_liste(bu,[1016,1018,1020,1022,1024,1027],5) == suma_liste(bu,[1017,1019,1021,1023,1025,1026],5) ):
            lzbir =  suma_liste(bu,[1016,1018,1020,1022,1024,1027],5) 
            dzbir =  suma_liste(bu,[1017,1019,1021,1023,1025,1026],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1016 + 1018 + 1020 + 1022 + 1024 + 1027) kol. 5 = AOP-u (1017 + 1019 + 1021 + 1023 + 1025 + 1026) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10057
        if not( suma_liste(bu,[1016,1018,1020,1022,1024,1027],6) == suma_liste(bu,[1017,1019,1021,1023,1025,1026],6) ):
            lzbir =  suma_liste(bu,[1016,1018,1020,1022,1024,1027],6) 
            dzbir =  suma_liste(bu,[1017,1019,1021,1023,1025,1026],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1016 + 1018 + 1020 + 1022 + 1024 + 1027) kol. 6 = AOP-u (1017 + 1019 + 1021 + 1023 + 1025 + 1026) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10058
        if not( suma_liste(bu,[1001,1008,1012,1018,1020,1022,1024,1027],5) == suma_liste(bu,[1002,1009,1013,1019,1021,1023,1025,1026],5) ):
            lzbir =  suma_liste(bu,[1001,1008,1012,1018,1020,1022,1024,1027],5) 
            dzbir =  suma_liste(bu,[1002,1009,1013,1019,1021,1023,1025,1026],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1008 + 1012 + 1018 + 1020 + 1022 + 1024 + 1027) kol. 5 = AOP-u (1002 + 1009 + 1013+ 1019 + 1021 + 1023 + 1025 + 1026) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10059
        if not( suma_liste(bu,[1001,1008,1012,1018,1020,1022,1024,1027],6) == suma_liste(bu,[1002,1009,1013,1019,1021,1023,1025,1026],6) ):
            lzbir =  suma_liste(bu,[1001,1008,1012,1018,1020,1022,1024,1027],6) 
            dzbir =  suma_liste(bu,[1002,1009,1013,1019,1021,1023,1025,1026],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1008 + 1012 + 1018 + 1020 + 1022 + 1024 + 1027) kol. 6 = AOP-u (1002 + 1009 + 1013+ 1019 + 1021 + 1023 + 1025 + 1026) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10060
        if not( aop(bu,1028,5) > 0 ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1028 kol. 5 > 0 Na poziciji Poreski rashod perioda nije iskazan podatak; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #10061
        if( suma_liste(bu,[1026,1030],5) > suma(bu,1027,1029,5) ):
            if not( aop(bu,1031,5) == suma_liste(bu,[1026,1030],5)-suma(bu,1027,1029,5) ):
                lzbir =  aop(bu,1031,5) 
                dzbir =  suma_liste(bu,[1026,1030],5)-suma(bu,1027,1029,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1031 kol. 5 = AOP-u (1026 - 1027 - 1028 - 1029 + 1030) kol. 5, ako je AOP (1026 + 1030) kol. 5 > AOP-a (1027 + 1028 + 1029) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10062
        if( suma_liste(bu,[1026,1030],6) > suma(bu,1027,1029,6) ):
            if not( aop(bu,1031,6) == suma_liste(bu,[1026,1030],6)-suma(bu,1027,1029,6) ):
                lzbir =  aop(bu,1031,6) 
                dzbir =  suma_liste(bu,[1026,1030],6)-suma(bu,1027,1029,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1031 kol. 6 = AOP-u (1026 - 1027 - 1028 - 1029 + 1030) kol. 6, ako je AOP (1026 + 1030) kol. 6 > AOP-a (1027 + 1028 + 1029) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10063
        if( suma_liste(bu,[1026,1030],5) < suma(bu,1027,1029,5) ):
            if not( aop(bu,1032,5) == suma(bu,1027,1029,5)-suma_liste(bu,[1026,1030],5) ):
                lzbir =  aop(bu,1032,5) 
                dzbir =  suma(bu,1027,1029,5)-suma_liste(bu,[1026,1030],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1032 kol. 5 = AOP-u (1027 - 1026 + 1028 + 1029 - 1030) kol. 5, ako je AOP (1026 + 1030) kol. 5 < AOP-a (1027 + 1028 + 1029) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10064
        if( suma_liste(bu,[1026,1030],6) < suma(bu,1027,1029,6) ):
            if not( aop(bu,1032,6) == suma(bu,1027,1029,6)-suma_liste(bu,[1026,1030],6) ):
                lzbir =  aop(bu,1032,6) 
                dzbir =  suma(bu,1027,1029,6)-suma_liste(bu,[1026,1030],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1032 kol. 6 = AOP-u (1027 - 1026 + 1028 + 1029 - 1030) kol. 6, ako je AOP (1026 + 1030) kol. 6 < AOP-a (1027 + 1028 + 1029) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10065
        if( suma_liste(bu,[1026,1030],5) == suma(bu,1027,1029,5) ):
            if not( suma(bu,1031,1032,5) == 0 ):
                lzbir =  suma(bu,1031,1032,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1031 + 1032) kol. 5 = 0, ako je AOP (1026 + 1030) kol. 5 = AOP-u (1027 + 1028 + 1029) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10066
        if( suma_liste(bu,[1026,1030],6) == suma(bu,1027,1029,6) ):
            if not( suma(bu,1031,1032,6) == 0 ):
                lzbir =  suma(bu,1031,1032,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1031 + 1032) kol. 6 = 0, ako je AOP (1026 + 1030) kol. 6 = AOP-u (1027 + 1028 + 1029) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10067
        if( aop(bu,1031,5) > 0 ):
            if not( aop(bu,1032,5) == 0 ):
                lzbir =  aop(bu,1032,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1031 kol. 5 > 0 onda je AOP 1032 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10068
        if( aop(bu,1032,5) > 0 ):
            if not( aop(bu,1031,5) == 0 ):
                lzbir =  aop(bu,1031,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1032 kol. 5 > 0 onda je AOP 1031 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10069
        if( aop(bu,1031,6) > 0 ):
            if not( aop(bu,1032,6) == 0 ):
                lzbir =  aop(bu,1032,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1031 kol. 6 > 0 onda je AOP 1032 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10070
        if( aop(bu,1032,6) > 0 ):
            if not( aop(bu,1031,6) == 0 ):
                lzbir =  aop(bu,1031,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1032 kol. 6 > 0 onda je AOP 1031 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10071
        if not( suma_liste(bu,[1026,1030,1032],5) == suma_liste(bu,[1027,1028,1029,1031],5) ):
            lzbir =  suma_liste(bu,[1026,1030,1032],5) 
            dzbir =  suma_liste(bu,[1027,1028,1029,1031],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1026 + 1030 + 1032) kol. 5 = AOP-u (1027 + 1028 + 1029 + 1031) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10072
        if not( suma_liste(bu,[1026,1030,1032],6) == suma_liste(bu,[1027,1028,1029,1031],6) ):
            lzbir =  suma_liste(bu,[1026,1030,1032],6) 
            dzbir =  suma_liste(bu,[1027,1028,1029,1031],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1026 + 1030 + 1032) kol. 6 = AOP-u (1027 + 1028 + 1029 + 1031) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10073
        #Za ovaj set se ne primenjuje pravilo 
        
        #10074
        #Za ovaj set se ne primenjuje pravilo 
        
        #10075
        #Za ovaj set se ne primenjuje pravilo 
        
        #10076
        #Za ovaj set se ne primenjuje pravilo 
        
        #10077
        if not( aop(bu,1033,5) == 0 ):
            lzbir =  aop(bu,1033,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1033 kol. 5 = 0 Neto dobitak koji pripada učešćima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10078
        if not( aop(bu,1033,6) == 0 ):
            lzbir =  aop(bu,1033,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1033 kol. 6 = 0 Neto dobitak koji pripada učešćima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10079
        if not( aop(bu,1034,5) == 0 ):
            lzbir =  aop(bu,1034,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1034 kol. 5 = 0 Neto dobitak koji pripada matičnom pravnom licu prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10080
        if not( aop(bu,1034,6) == 0 ):
            lzbir =  aop(bu,1034,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1034 kol. 6 = 0 Neto dobitak koji pripada matičnom pravnom licu prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10081
        if not( aop(bu,1035,5) == 0 ):
            lzbir =  aop(bu,1035,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1035 kol. 5 = 0 Neto gubitak koji pripada učešćima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10082
        if not( aop(bu,1035,6) == 0 ):
            lzbir =  aop(bu,1035,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1035 kol. 6 = 0 Neto gubitak koji pripada učešćima bez prava kontrole prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10083
        if not( aop(bu,1036,5) == 0 ):
            lzbir =  aop(bu,1036,5) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1036 kol. 5 = 0 Neto gubitak koji pripada matičnom pravnom licu prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10084
        if not( aop(bu,1036,6) == 0 ):
            lzbir =  aop(bu,1036,6) 
            dzbir =  0 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1036 kol. 6 = 0 Neto gubitak koji pripada matičnom pravnom licu prikazuje se samo u konsolidovanom FI '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10085
        if( aop(bu,1031,5) > 0 ):
            if not( aop(bs,413,5) == aop(bu,1031,5) ):
                lzbir =  aop(bs,413,5) 
                dzbir =  aop(bu,1031,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1031 kol. 5 > 0, onda je AOP 0413 kol. 5 bilansa stanja = AOP-u 1031 kol. 5  Neto dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu neraspoređenog dobitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1031 kol. 5 > 0, onda je AOP 0413 kol. 5 bilansa stanja = AOP-u 1031 kol. 5  Neto dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu neraspoređenog dobitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10086
        if( aop(bs,413,5) > 0 ):
            if not( aop(bu,1031,5) == aop(bs,413,5) ):
                lzbir =  aop(bu,1031,5) 
                dzbir =  aop(bs,413,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0413 kol. 5 bilansa stanja > 0, onda je AOP 1031 kol. 5 bilansa uspeha = AOP-u 0413 kol. 5 bilansa stanja  Neto dobitak tekuće godine u obrascu Bilans uspeha po pravilu mora biti jednak prikazanom iznosu neraspoređenog dobitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 0413 kol. 5 bilansa stanja > 0, onda je AOP 1031 kol. 5 bilansa uspeha = AOP-u 0413 kol. 5 bilansa stanja  Neto dobitak tekuće godine u obrascu Bilans uspeha po pravilu mora biti jednak prikazanom iznosu neraspoređenog dobitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10087
        if( aop(bu,1031,6) > 0 ):
            if not( aop(bs,413,6) == aop(bu,1031,6) ):
                lzbir =  aop(bs,413,6) 
                dzbir =  aop(bu,1031,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1031 kol. 6 > 0, onda je AOP 0413 kol. 6 bilansa stanja = AOP-a 1031 kol. 6 Neto dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak   neraspoređenom dobitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1031 kol. 6 > 0, onda je AOP 0413 kol. 6 bilansa stanja = AOP-a 1031 kol. 6 Neto dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak   neraspoređenom dobitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10088
        if( aop(bs,413,6) > 0 ):
            if not( aop(bu,1031,6) == aop(bs,413,6) ):
                lzbir =  aop(bu,1031,6) 
                dzbir =  aop(bs,413,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0413 kol. 6 bilansa stanja > 0, onda je AOP-u 1031 kol. 6 bilansa uspeha = AOP-u 0413 kol. 6 bilansa stanja  Neto dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak   neraspoređenom dobitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 0413 kol. 6 bilansa stanja > 0, onda je AOP-u 1031 kol. 6 bilansa uspeha = AOP-u 0413 kol. 6 bilansa stanja  Neto dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak   neraspoređenom dobitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10089
        if( aop(bu,1032,5) > 0 ):
            if not( aop(bs,417,5) == aop(bu,1032,5) ):
                lzbir =  aop(bs,417,5) 
                dzbir =  aop(bu,1032,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1032 kol. 5 > 0, onda je AOP 0417 kol. 5 bilansa stanja = AOP-a 1032 kol. 5 Neto gubitak tekuće godine u obrascu Bilans uspeha po pravilu mora biti jednak prikazanom iznosu gubitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1032 kol. 5 > 0, onda je AOP 0417 kol. 5 bilansa stanja = AOP-a 1032 kol. 5 Neto gubitak tekuće godine u obrascu Bilans uspeha po pravilu mora biti jednak prikazanom iznosu gubitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10090
        if( aop(bs,417,5) > 0 ):
            if not( aop(bu,1032,5) == aop(bs,417,5) ):
                lzbir =  aop(bu,1032,5) 
                dzbir =  aop(bs,417,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0417 kol. 5 bilansa stanja > 0, onda je AOP 1032 kol. 5 bilansa uspeha = AOP-u 0417 kol. 5 bilansa stanja Neto gubitak tekuće godine u obrascu Bilans uspeha po pravilu mora biti jednak prikazanom iznosu gubitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 0417 kol. 5 bilansa stanja > 0, onda je AOP 1032 kol. 5 bilansa uspeha = AOP-u 0417 kol. 5 bilansa stanja Neto gubitak tekuće godine u obrascu Bilans uspeha po pravilu mora biti jednak prikazanom iznosu gubitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10091
        if( aop(bu,1032,6) > 0 ):
            if not( aop(bs,417,6) == aop(bu,1032,6) ):
                lzbir =  aop(bs,417,6) 
                dzbir =  aop(bu,1032,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1032 kol. 6 bilansa uspeha > 0, onda  je AOP 0417 kol. 6 bilansa stanja = AOP-u 1032 kol. 6  bilansa uspeha Neto gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak  gubitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1032 kol. 6 bilansa uspeha > 0, onda  je AOP 0417 kol. 6 bilansa stanja = AOP-u 1032 kol. 6  bilansa uspeha Neto gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak  gubitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10092
        if( aop(bs,417,6) > 0 ):
            if not( aop(bu,1032,6) == aop(bs,417,6) ):
                lzbir =  aop(bu,1032,6) 
                dzbir =  aop(bs,417,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0417 kol. 6 bilansa stanja > 0, onda je AOP 1032 kol. 6 bilansa uspeha = AOP-u 0417 kol. 6 bilansa stanja Neto gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak  gubitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 0417 kol. 6 bilansa stanja > 0, onda je AOP 1032 kol. 6 bilansa uspeha = AOP-u 0417 kol. 6 bilansa stanja Neto gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak  gubitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10093
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if( suma(bu,1001,1038,5) > 0 ):
                if not( suma(bu,1001,1038,5) != suma(bu,1001,1038,6) ):
                    
                    naziv_obrasca='Bilans uspeha'
                    poruka  ='***Ako je zbir podataka na oznakama za AOP (1001 do 1038) kol. 5 > 0 onda zbir podataka na oznakama za AOP (1001 do 1038) kol. 5 ≠ zbiru podataka na oznakama za AOP  (1001 do 1038) kol. 6 Zbirovi podataka u kolonama 5 i 6 bilansa uspeha su identični; Proverite ispravnost unetih podataka na pojedinačnim AOP pozicijama u tim kolonama;  '
                    aop_pozicije=[]
                    poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                    form_warnings.append(poruka_obrasca)
        
        
        ######################################
        #### KRAJ KONTROLNIH PRAVILA    ######
        ######################################

        return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}

    except Exception as e:
        #trace = traceback.format_exc() #traceback.print_tb(sys.exc_info()[2])
        trace=''
        errorMsg = e.message

        exceptionList.append({'errorMessage':errorMsg, 'trace':trace})
        
        return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}


