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

        #S milošem proveriti
        '''
        fia = getForme(Zahtev,'Finansijski izveštaj OIF 1')
        if len(fia)==0:
            
            naziv_obrasca='Finansijski izveštaj DPF 1'
            poruka  ='Finansijski izveštaj OIF 1 nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        fib = getForme(Zahtev,'Finansijski izveštaj OIF 2')
        if len(fib)==0:
            
            naziv_obrasca='Finansijski izveštaj DPF 2'
            poruka  ='Finansijski izveštaj OIF 2 nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        fic = getForme(Zahtev,'Finansijski izveštaj OIF 3')
        if len(fic)==0:
            
            naziv_obrasca='Finansijski izveštaj DPF 3'
            poruka  ='Finansijski izveštaj OIF 3 nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
            
        fid = getForme(Zahtev,'Finansijski izveštaj OIF 4')
        if len(fid)==0:
            
            naziv_obrasca='Finansijski izveštaj DPF 4'
            poruka  ='Finansijski izveštaj OIF 4 nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        fie = getForme(Zahtev,'Finansijski izveštaj OIF 5')
        if len(fie)==0:
            
            naziv_obrasca='Finansijski izveštaj DPF 5'
            poruka  ='Finansijski izveštaj OIF 5 nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)

        fif = getForme(Zahtev,'Finansijski izveštaj OIF 6')
        if len(fif)==0:
            naziv_obrasca='Obrazac'
            poruka  ='Finansijski izveštaj OIF 6 nije popunjen'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        '''    

        if len(form_errors)>0:
            return {'doc_errors': doc_errors, 'doc_warnings': doc_warnings, 'form_warnings':form_warnings,'form_errors':form_errors,'ostalo_errors':ostalo_errors, 'ostalo_warnings':ostalo_warnings, 'exceptions' : exceptionList}
        

        lzbir = 0
        dzbir = 0
        razlika = 0

        hasError = False
        hasWarning = False

        ######################################
        #### POCETAK KONTROLNIH PRAVILA ######
        ######################################


        
        #00000-1
        #Za ovaj set se ne primenjuje pravilo 
        
        #00000-2
        if not( suma(bs,1,23,5)+suma(bs,1,23,6)+suma(bs,1,23,7)+suma(bs,401,440,5)+suma(bs,401,440,6)+suma(bs,401,440,7)+suma(bu,1001,1031,5)+suma(bu,1001,1031,6) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0023) kol. 5  + (0001 do 0023) kol. 6 + (0001 do 0023) kol. 7 bilansa stanja + (0401 do 0440) kol. 5 + (0401 do 0440) kol. 6 + (0401 do 0440) kol. 7 bilansa stanja  + (1001 do 1031) kol. 5 + (1001 do 1031) kol. 6 bilansa uspeha > 0 Vanredni finansijski izveštaj, po pravilu ne sme biti bez podataka; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP od (0001 do 0023) kol. 5  + (0001 do 0023) kol. 6 + (0001 do 0023) kol. 7 bilansa stanja + (0401 do 0440) kol. 5 + (0401 do 0440) kol. 6 + (0401 do 0440) kol. 7 bilansa stanja  + (1001 do 1031) kol. 5 + (1001 do 1031) kol. 6 bilansa uspeha > 0 Vanredni finansijski izveštaj, po pravilu ne sme biti bez podataka; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga'
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #Provera da li je fizahtev placen
        if not(Zahtev.Placen):
            ostalo_errors.append('Naknada za obradu i javno objavljivanje izveštaja i propisane dokumentacije nije uplaćena u propisanom iznosu. Instrukcije za uplatu propisane naknade date su u okviru PIS FI sistema za konkretan zahtev, na linku „Status naplate zahteva / Instrukcija za plaćanje". Ukoliko ste izvršili uplatu, a naknada nije uparena, priložite Dokaz o uplati naknade u delu Dokumentacija (na mestu predviđenom za dokaz o uplati naknade), kako biste mogli da podnesete izveštaj.');

        #Provera negativnih AOP-a
        lista=""
        lista_bs = find_negativni(bs, 1, 440, 5, 7)
        lista_bu = find_negativni(bu, 1001, 1032, 5, 6)
        

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

        
        #00000-3
        #Za ovaj set se ne primenjuje pravilo 
        
        #BILANS STANJA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #00001
        if not( suma(bs,1,23,5)+suma(bs,401,440,5) > 0 ):
            
            naziv_obrasca='Bilans stanja'
            poruka  ='Zbir podataka na oznakama za AOP (0001 do 0023) kol. 5 + (0401 do 0440) kol. 5 > 0 Bilans stanja, po pravilu, mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #00002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,23,6)+suma(bs,401,440,6) == 0 ):
                lzbir =  suma(bs,1,23,6)+suma(bs,401,440,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0023) kol. 6 + (0401 do 0440) kol. 6 = 0 Bilans stanja za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00003
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bs,1,23,7)+suma(bs,401,440,7) == 0 ):
                lzbir =  suma(bs,1,23,7)+suma(bs,401,440,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0023) kol. 7 + (0401 do 0440) kol. 7 = 0 Bilans stanja za novoosnovane obveznike  ne sme imati iskazano početno stanje za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00004
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,23,6)+suma(bs,401,440,6) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0023) kol. 6 + (0401 do 0440) kol. 6 > 0 Bilans stanja, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00005
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bs,1,23,7)+suma(bs,401,440,7) > 0 ):
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Zbir podataka na oznakama za AOP (0001 do 0023) kol. 7 + (0401 do 0440) kol. 7 > 0 Bilans stanja, po pravilu,  mora imati iskazano početno stanje za prethodni izveštajni period za obveznike koji vrše reklasifikaciju; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #00006
        if not( aop(bs,4,5) == suma(bs,5,7,5) ):
            lzbir =  aop(bs,4,5) 
            dzbir =  suma(bs,5,7,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0004 kol. 5 = AOP-u (0005 + 0006 + 0007) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00007
        if not( aop(bs,4,6) == suma(bs,5,7,6) ):
            lzbir =  aop(bs,4,6) 
            dzbir =  suma(bs,5,7,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0004 kol. 6 = AOP-u (0005 + 0006 + 0007) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00008
        if not( aop(bs,4,7) == suma(bs,5,7,7) ):
            lzbir =  aop(bs,4,7) 
            dzbir =  suma(bs,5,7,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0004 kol. 7 = AOP-u (0005 + 0006 + 0007) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00009
        if not( aop(bs,10,5) == suma(bs,11,18,5) ):
            lzbir =  aop(bs,10,5) 
            dzbir =  suma(bs,11,18,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0010 kol. 5 = AOP-u (0011 + 0012 + 0013 + 0014 + 0015 + 0016 + 0017 + 0018) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00010
        if not( aop(bs,10,6) == suma(bs,11,18,6) ):
            lzbir =  aop(bs,10,6) 
            dzbir =  suma(bs,11,18,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0010 kol. 6 = AOP-u (0011 + 0012 + 0013 + 0014 + 0015 + 0016 + 0017 + 0018) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00011
        if not( aop(bs,10,7) == suma(bs,11,18,7) ):
            lzbir =  aop(bs,10,7) 
            dzbir =  suma(bs,11,18,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0010 kol. 7 = AOP-u (0011 + 0012 + 0013 + 0014 + 0015 + 0016 + 0017 + 0018) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00012
        if not( aop(bs,22,5) == suma_liste(bs,[1,2,3,4,8,9,10,19,20,21],5) ):
            lzbir =  aop(bs,22,5) 
            dzbir =  suma_liste(bs,[1,2,3,4,8,9,10,19,20,21],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0022 kol. 5 = AOP-u (0001 + 0002 + 0003 + 0004 + 0008 + 0009 + 0010 + 0019 + 0020 + 0021) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00013
        if not( aop(bs,22,6) == suma_liste(bs,[1,2,3,4,8,9,10,19,20,21],6) ):
            lzbir =  aop(bs,22,6) 
            dzbir =  suma_liste(bs,[1,2,3,4,8,9,10,19,20,21],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0022 kol. 6 = AOP-u (0001 + 0002 + 0003 + 0004 + 0008 + 0009 + 0010 + 0019 + 0020 + 0021) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00014
        if not( aop(bs,22,7) == suma_liste(bs,[1,2,3,4,8,9,10,19,20,21],7) ):
            lzbir =  aop(bs,22,7) 
            dzbir =  suma_liste(bs,[1,2,3,4,8,9,10,19,20,21],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0022 kol. 7 = AOP-u (0001 + 0002 + 0003 + 0004 + 0008 + 0009 + 0010 + 0019 + 0020 + 0021) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00015
        if( suma_liste(bs,[402,404,405,406,407,409],5) > suma_liste(bs,[403,408,412,415],5) ):
            if not( aop(bs,401,5) == suma_liste(bs,[402,404,405,406,407,409],5)-suma_liste(bs,[403,408,412,415],5) ):
                lzbir =  aop(bs,401,5) 
                dzbir =  suma_liste(bs,[402,404,405,406,407,409],5)-suma_liste(bs,[403,408,412,415],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 5 = AOP-u (0402 - 0403 + 0404 + 0405 + 0406 + 0407 - 0408 + 0409 - 0412 - 0415) kol. 5, ako je AOP (0402 + 0404 + 0405 + 0406 + 0407 + 0409) kol. 5 > AOP-a (0403 + 0408 + 0412 + 0415) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00016
        if( suma_liste(bs,[402,404,405,406,407,409],6) > suma_liste(bs,[403,408,412,415],6) ):
            if not( aop(bs,401,6) == suma_liste(bs,[402,404,405,406,407,409],6)-suma_liste(bs,[403,408,412,415],6) ):
                lzbir =  aop(bs,401,6) 
                dzbir =  suma_liste(bs,[402,404,405,406,407,409],6)-suma_liste(bs,[403,408,412,415],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 6 = AOP-u (0402 - 0403 + 0404 + 0405 + 0406 + 0407 - 0408 + 0409 - 0412 - 0415) kol. 6, ako je AOP (0402 + 0404 + 0405 + 0406 + 0407 + 0409) kol. 6 > AOP-a (0403 + 0408 + 0412 + 0415) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00017
        if( suma_liste(bs,[402,404,405,406,407,409],7) > suma_liste(bs,[403,408,412,415],7) ):
            if not( aop(bs,401,7) == suma_liste(bs,[402,404,405,406,407,409],7)-suma_liste(bs,[403,408,412,415],7) ):
                lzbir =  aop(bs,401,7) 
                dzbir =  suma_liste(bs,[402,404,405,406,407,409],7)-suma_liste(bs,[403,408,412,415],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 7 = AOP-u (0402 - 0403 + 0404 + 0405 + 0406 + 0407 - 0408 + 0409 - 0412 - 0415) kol. 7, ako je AOP (0402 + 0404 + 0405 + 0406 + 0407 + 0409) kol. 7 > AOP-a (0403 + 0408 + 0412 + 0415) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00018
        if( aop(bs,22,5) > suma_liste(bs,[416,434,435,436,437],5) ):
            if not( aop(bs,401,5) == aop(bs,22,5)-suma_liste(bs,[416,434,435,436,437],5) ):
                lzbir =  aop(bs,401,5) 
                dzbir =  aop(bs,22,5)-suma_liste(bs,[416,434,435,436,437],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 5 = AOP-u (0022 - 0416 - 0434 - 0435 - 0436 - 0437) kol. 5, ako je AOP 0022 kol. 5 > AOP-a (0416 + 0434 + 0435 + 0436 + 0437) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00019
        if( aop(bs,22,6) > suma_liste(bs,[416,434,435,436,437],6) ):
            if not( aop(bs,401,6) == aop(bs,22,6)-suma_liste(bs,[416,434,435,436,437],6) ):
                lzbir =  aop(bs,401,6) 
                dzbir =  aop(bs,22,6)-suma_liste(bs,[416,434,435,436,437],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 6 = AOP-u (0022 - 0416 - 0434 - 0435 - 0436 - 0437) kol. 6, ako je AOP 0022 kol. 6 > AOP-a (0416 + 0434 + 0435 + 0436 + 0437) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00020
        if( aop(bs,22,7) > suma_liste(bs,[416,434,435,436,437],7) ):
            if not( aop(bs,401,7) == aop(bs,22,7)-suma_liste(bs,[416,434,435,436,437],7) ):
                lzbir =  aop(bs,401,7) 
                dzbir =  aop(bs,22,7)-suma_liste(bs,[416,434,435,436,437],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0401 kol. 7 = AOP-u (0022 - 0416 - 0434 - 0435 - 0436 - 0437) kol. 7, ako je AOP 0022 kol. 7 > AOP-a (0416 + 0434 + 0435 + 0436 + 0437) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00021
        if not( aop(bs,409,5) == suma(bs,410,411,5) ):
            lzbir =  aop(bs,409,5) 
            dzbir =  suma(bs,410,411,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0409 kol. 5 = AOP-u (0410 + 0411) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00022
        if not( aop(bs,409,6) == suma(bs,410,411,6) ):
            lzbir =  aop(bs,409,6) 
            dzbir =  suma(bs,410,411,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0409 kol. 6 = AOP-u (0410 + 0411) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00023
        if not( aop(bs,409,7) == suma(bs,410,411,7) ):
            lzbir =  aop(bs,409,7) 
            dzbir =  suma(bs,410,411,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0409 kol. 7 = AOP-u (0410 + 0411) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00024
        if not( aop(bs,412,5) == suma(bs,413,414,5) ):
            lzbir =  aop(bs,412,5) 
            dzbir =  suma(bs,413,414,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0412 kol. 5 = AOP-u (0413 + 0414) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00025
        if not( aop(bs,412,6) == suma(bs,413,414,6) ):
            lzbir =  aop(bs,412,6) 
            dzbir =  suma(bs,413,414,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0412 kol. 6 = AOP-u (0413 + 0414) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00026
        if not( aop(bs,412,7) == suma(bs,413,414,7) ):
            lzbir =  aop(bs,412,7) 
            dzbir =  suma(bs,413,414,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0412 kol. 7 = AOP-u (0413 + 0414) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00027
        if not( aop(bs,416,5) == suma_liste(bs,[417,418,428,433],5) ):
            lzbir =  aop(bs,416,5) 
            dzbir =  suma_liste(bs,[417,418,428,433],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0416 kol. 5 = AOP-u (0417 + 0418 + 0428 + 0433) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00028
        if not( aop(bs,416,6) == suma_liste(bs,[417,418,428,433],6) ):
            lzbir =  aop(bs,416,6) 
            dzbir =  suma_liste(bs,[417,418,428,433],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0416 kol. 6 = AOP-u (0417 + 0418 + 0428 + 0433) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00029
        if not( aop(bs,416,7) == suma_liste(bs,[417,418,428,433],7) ):
            lzbir =  aop(bs,416,7) 
            dzbir =  suma_liste(bs,[417,418,428,433],7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0416 kol. 7 = AOP-u (0417 + 0418 + 0428 + 0433) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00030
        if not( aop(bs,418,5) == suma(bs,419,427,5) ):
            lzbir =  aop(bs,418,5) 
            dzbir =  suma(bs,419,427,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0418 kol. 5 = AOP-u (0419 + 0420 + 0421 + 0422 + 0423 + 0424 + 0425 + 0426 + 0427) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00031
        if not( aop(bs,418,6) == suma(bs,419,427,6) ):
            lzbir =  aop(bs,418,6) 
            dzbir =  suma(bs,419,427,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0418 kol. 6 = AOP-u (0419 + 0420 + 0421 + 0422 + 0423 + 0424 + 0425 + 0426 + 0427) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00032
        if not( aop(bs,418,7) == suma(bs,419,427,7) ):
            lzbir =  aop(bs,418,7) 
            dzbir =  suma(bs,419,427,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0418 kol. 7 = AOP-u (0419 + 0420 + 0421 + 0422 + 0423 + 0424 + 0425 + 0426 + 0427) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00033
        if not( aop(bs,428,5) == suma(bs,429,432,5) ):
            lzbir =  aop(bs,428,5) 
            dzbir =  suma(bs,429,432,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0428 kol. 5 = AOP-u (0429 + 0430 + 0431 + 0432) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00034
        if not( aop(bs,428,6) == suma(bs,429,432,6) ):
            lzbir =  aop(bs,428,6) 
            dzbir =  suma(bs,429,432,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0428 kol. 6 = AOP-u (0429 + 0430 + 0431 + 0432) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00035
        if not( aop(bs,428,7) == suma(bs,429,432,7) ):
            lzbir =  aop(bs,428,7) 
            dzbir =  suma(bs,429,432,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0428 kol. 7 = AOP-u (0429 + 0430 + 0431 + 0432) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00036
        if( suma_liste(bs,[402,404,405,406,407,409],5) < suma_liste(bs,[403,408,412,415],5) ):
            if not( aop(bs,438,5) == suma_liste(bs,[403,408,412,415],5)-suma_liste(bs,[402,404,405,406,407,409],5) ):
                lzbir =  aop(bs,438,5) 
                dzbir =  suma_liste(bs,[403,408,412,415],5)-suma_liste(bs,[402,404,405,406,407,409],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0438 kol. 5 = AOP-u (0403 - 0402 - 0404 - 0405 - 0406 - 0407 + 0408 - 0409 + 0412 + 0415) kol. 5, ako je AOP (0402 + 0404 + 0405 + 0406 + 0407 + 0409) kol. 5 < AOP-a (0403 + 0408 + 0412 + 0415) kol. 5   '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00037
        if( suma_liste(bs,[402,404,405,406,407,409],6) < suma_liste(bs,[403,408,412,415],6) ):
            if not( aop(bs,438,6) == suma_liste(bs,[403,408,412,415],6)-suma_liste(bs,[402,404,405,406,407,409],6) ):
                lzbir =  aop(bs,438,6) 
                dzbir =  suma_liste(bs,[403,408,412,415],6)-suma_liste(bs,[402,404,405,406,407,409],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0438 kol. 6 = AOP-u (0403 - 0402 - 0404 - 0405 - 0406 - 0407 + 0408 - 0409 + 0412 + 0415) kol. 6, ako je AOP (0402 + 0404 + 0405 + 0406 + 0407 + 0409) kol. 6 < AOP-a (0403 + 0408 + 0412 + 0415) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00038
        if( suma_liste(bs,[402,404,405,406,407,409],7) < suma_liste(bs,[403,408,412,415],7) ):
            if not( aop(bs,438,7) == suma_liste(bs,[403,408,412,415],7)-suma_liste(bs,[402,404,405,406,407,409],7) ):
                lzbir =  aop(bs,438,7) 
                dzbir =  suma_liste(bs,[403,408,412,415],7)-suma_liste(bs,[402,404,405,406,407,409],7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0438 kol. 7 = AOP-u (0403 - 0402 - 0404 - 0405 - 0406 - 0407 + 0408 - 0409 + 0412 + 0415) kol. 7, ako je AOP (0402 + 0404 + 0405 + 0406 + 0407 + 0409) kol. 7 < AOP-a (0403 + 0408 + 0412 + 0415) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00039
        if( aop(bs,22,5) < suma_liste(bs,[416,434,435,436,437],5) ):
            if not( aop(bs,438,5) == suma_liste(bs,[416,434,435,436,437],5)-aop(bs,22,5) ):
                lzbir =  aop(bs,438,5) 
                dzbir =  suma_liste(bs,[416,434,435,436,437],5)-aop(bs,22,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0438 kol. 5 = AOP-u (0416 + 0434 + 0435 + 0436 + 0437 - 0022) kol. 5, ako je AOP 0022 kol. 5 < AOP-a (0416 + 0434 + 0435 + 0436 + 0437) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00040
        if( aop(bs,22,6) < suma_liste(bs,[416,434,435,436,437],6) ):
            if not( aop(bs,438,6) == suma_liste(bs,[416,434,435,436,437],6)-aop(bs,22,6) ):
                lzbir =  aop(bs,438,6) 
                dzbir =  suma_liste(bs,[416,434,435,436,437],6)-aop(bs,22,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0438 kol. 6 = AOP-u (0416 + 0434 + 0435 + 0436 + 0437 - 0022) kol. 6, ako je AOP 0022 kol. 6 < AOP-a (0416 + 0434 + 0435 + 0436 + 0437) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00041
        if( aop(bs,22,7) < suma_liste(bs,[416,434,435,436,437],7) ):
            if not( aop(bs,438,7) == suma_liste(bs,[416,434,435,436,437],7)-aop(bs,22,7) ):
                lzbir =  aop(bs,438,7) 
                dzbir =  suma_liste(bs,[416,434,435,436,437],7)-aop(bs,22,7) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP 0438 kol. 7 = AOP-u (0416 + 0434 + 0435 + 0436 + 0437 - 0022) kol. 7, ako je AOP 0022 kol. 7 < AOP-a (0416 + 0434 + 0435 + 0436 + 0437) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00042
        if( suma_liste(bs,[402,404,405,406,407,409],5) == suma_liste(bs,[403,408,412,415],5) ):
            if not( suma_liste(bs,[401,438],5) == 0 ):
                lzbir =  suma_liste(bs,[401,438],5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0438 ) kol. 5 = 0, ako je AOP (0402 + 0404 + 0405 + 0406 + 0407 + 0409) kol. 5 = AOP-u (0403 + 0408 + 0412 + 0415) kol. 5  Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00043
        if( suma_liste(bs,[402,404,405,406,407,409],6) == suma_liste(bs,[403,408,412,415],6) ):
            if not( suma_liste(bs,[401,438],6) == 0 ):
                lzbir =  suma_liste(bs,[401,438],6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0438 ) kol. 6 = 0, ako je AOP (0402 + 0404 + 0405 + 0406 + 0407 + 0409) kol. 6 = AOP-u (0403 + 0408 + 0412 + 0415) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00044
        if( suma_liste(bs,[402,404,405,406,407,409],7) == suma_liste(bs,[403,408,412,415],7) ):
            if not( suma_liste(bs,[401,438],7) == 0 ):
                lzbir =  suma_liste(bs,[401,438],7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0438 ) kol. 7 = 0, ako je AOP (0402 + 0404 + 0405 + 0406 + 0407 + 0409) kol. 7 = AOP-u (0403 + 0408 + 0412 + 0415) kol. 7 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00045
        if( aop(bs,22,5) == suma_liste(bs,[416,434,435,436,437],5) ):
            if not( suma_liste(bs,[401,438],5) == 0 ):
                lzbir =  suma_liste(bs,[401,438],5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0438 ) kol. 5 = 0, ako je AOP 0022 kol. 5 = AOP-u (0416 + 0434 + 0435 + 0436 + 0437) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00046
        if( aop(bs,22,6) == suma_liste(bs,[416,434,435,436,437],6) ):
            if not( suma_liste(bs,[401,438],6) == 0 ):
                lzbir =  suma_liste(bs,[401,438],6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0438 ) kol. 6 = 0, ako je AOP 0022 kol. 6 = AOP-u (0416 + 0434 + 0435 + 0436 + 0437) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00047
        if( aop(bs,22,7) == suma_liste(bs,[416,434,435,436,437],7) ):
            if not( suma_liste(bs,[401,438],7) == 0 ):
                lzbir =  suma_liste(bs,[401,438],7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='AOP (0401 + 0438 ) kol. 7 = 0, ako je AOP 0022 kol. 7 = AOP-u (0416 + 0434 + 0435 + 0436 + 0437) kol. 7 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00048
        if( aop(bs,401,5) > 0 ):
            if not( aop(bs,438,5) == 0 ):
                lzbir =  aop(bs,438,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 5 > 0 onda je AOP 0438 kol. 5 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00049
        if( aop(bs,438,5) > 0 ):
            if not( aop(bs,401,5) == 0 ):
                lzbir =  aop(bs,401,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0438 kol. 5 > 0 onda je AOP 0401 kol. 5 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00050
        if( aop(bs,401,6) > 0 ):
            if not( aop(bs,438,6) == 0 ):
                lzbir =  aop(bs,438,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 6 > 0 onda je AOP 0438 kol. 6 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00051
        if( aop(bs,438,6) > 0 ):
            if not( aop(bs,401,6) == 0 ):
                lzbir =  aop(bs,401,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0438 kol. 6 > 0 onda je AOP 0401 kol. 6 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00052
        if( aop(bs,401,7) > 0 ):
            if not( aop(bs,438,7) == 0 ):
                lzbir =  aop(bs,438,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0401 kol. 7 > 0 onda je AOP 0438 kol. 7 = 0  Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00053
        if( aop(bs,438,7) > 0 ):
            if not( aop(bs,401,7) == 0 ):
                lzbir =  aop(bs,401,7) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0438 kol. 7 > 0 onda je AOP 0401 kol. 7 = 0 Ne mogu biti istovremeno prikazani ukupni kapital i gubitak iznad visine kapitala '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #00054
        if not( aop(bs,439,5) == suma_liste(bs,[401,416,434,435,436,437],5)-aop(bs,438,5) ):
            lzbir =  aop(bs,439,5) 
            dzbir =  suma_liste(bs,[401,416,434,435,436,437],5)-aop(bs,438,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0439 kol. 5 = AOP-u (0401 + 0416 + 0434 + 0435 + 0436 + 0437 - 0438) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00055
        if not( aop(bs,439,6) == suma_liste(bs,[401,416,434,435,436,437],6)-aop(bs,438,6) ):
            lzbir =  aop(bs,439,6) 
            dzbir =  suma_liste(bs,[401,416,434,435,436,437],6)-aop(bs,438,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0439 kol. 6 = AOP-u (0401 + 0416 + 0434 + 0435 + 0436 + 0437 - 0438) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00056
        if not( aop(bs,439,7) == suma_liste(bs,[401,416,434,435,436,437],7)-aop(bs,438,7) ):
            lzbir =  aop(bs,439,7) 
            dzbir =  suma_liste(bs,[401,416,434,435,436,437],7)-aop(bs,438,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0439 kol. 7 = AOP-u (0401 + 0416 + 0434 + 0435 + 0436 + 0437 - 0438) kol. 7  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00057
        if not( aop(bs,22,5) == aop(bs,439,5) ):
            lzbir =  aop(bs,22,5) 
            dzbir =  aop(bs,439,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0022 kol. 5 = AOP-u 0439 kol. 5 Kontrolni pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00058
        if not( aop(bs,22,6) == aop(bs,439,6) ):
            lzbir =  aop(bs,22,6) 
            dzbir =  aop(bs,439,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0022 kol. 6 = AOP-u 0439 kol. 6 Kontrolni pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00059
        if not( aop(bs,22,7) == aop(bs,439,7) ):
            lzbir =  aop(bs,22,7) 
            dzbir =  aop(bs,439,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0022 kol. 7 = AOP-u 0439 kol. 7 Kontrolni pravilo zahteva slaganje bilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00060
        if not( aop(bs,23,5) == aop(bs,440,5) ):
            lzbir =  aop(bs,23,5) 
            dzbir =  aop(bs,440,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0023 kol. 5 = AOP-u 0440 kol. 5 Kontrolni pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00061
        if not( aop(bs,23,6) == aop(bs,440,6) ):
            lzbir =  aop(bs,23,6) 
            dzbir =  aop(bs,440,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0023 kol. 6 = AOP-u 0440 kol. 6 Kontrolni pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #00062
        if not( aop(bs,23,7) == aop(bs,440,7) ):
            lzbir =  aop(bs,23,7) 
            dzbir =  aop(bs,440,7) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans stanja'
            poruka  ='AOP 0023 kol. 7 = AOP-u 0440 kol. 7 Kontrolni pravilo zahteva slaganje vanbilansne aktive i pasive '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #BILANS USPEHA - NA AOP POZICIJAMA NE MOGU BITI ISKAZANI NEGATIVNI IZNOSI
        
        #10001
        if not( suma(bu,1001,1031,5) > 0 ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='Zbir podataka na oznakama za AOP (1001 do 1031) kol. 5 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za tekući izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #10002
        if(Zahtev.ObveznikInfo.Novoosnovan == True): 
            if not( suma(bu,1001,1031,6) == 0 ):
                lzbir =  suma(bu,1001,1031,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1031) kol. 6 = 0 Bilans uspeha za novoosnovane obveznike ne sme imati iskazane podatke za prethodni izveštajni period; '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10003
        if(Zahtev.ObveznikInfo.Novoosnovan == False): 
            if not( suma(bu,1001,1031,6) > 0 ):
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Zbir podataka na oznakama za AOP (1001 do 1031) kol. 6 > 0 Bilans uspeha, po pravilu,  mora imati iskazane podatke za prethodni izveštajni period; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10004
        if not( aop(bu,1001,5) == suma(bu,1002,1004,5) ):
            lzbir =  aop(bu,1001,5) 
            dzbir =  suma(bu,1002,1004,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1001 kol. 5 = AOP-u (1002 + 1003 + 1004) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10005
        if not( aop(bu,1001,6) == suma(bu,1002,1004,6) ):
            lzbir =  aop(bu,1001,6) 
            dzbir =  suma(bu,1002,1004,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1001 kol. 6 = AOP-u (1002 + 1003 + 1004) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10006
        if not( aop(bu,1005,5) == suma(bu,1006,1010,5) ):
            lzbir =  aop(bu,1005,5) 
            dzbir =  suma(bu,1006,1010,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1005 kol. 5 = AOP-u (1006 + 1007 + 1008 + 1009 + 1010) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10007
        if not( aop(bu,1005,6) == suma(bu,1006,1010,6) ):
            lzbir =  aop(bu,1005,6) 
            dzbir =  suma(bu,1006,1010,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1005 kol. 6 = AOP-u (1006 + 1007 + 1008 + 1009 + 1010) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10008
        if( aop(bu,1001,5) > aop(bu,1005,5) ):
            if not( aop(bu,1011,5) == aop(bu,1001,5)-aop(bu,1005,5) ):
                lzbir =  aop(bu,1011,5) 
                dzbir =  aop(bu,1001,5)-aop(bu,1005,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1011 kol. 5 = AOP-u (1001 - 1005) kol. 5, ako je AOP 1001 kol. 5 > AOP-a 1005 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10009
        if( aop(bu,1001,6) > aop(bu,1005,6) ):
            if not( aop(bu,1011,6) == aop(bu,1001,6)-aop(bu,1005,6) ):
                lzbir =  aop(bu,1011,6) 
                dzbir =  aop(bu,1001,6)-aop(bu,1005,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1011 kol. 6 = AOP-u (1001 - 1005) kol. 6, ako je AOP 1001 kol. 6 > AOP-a 1005 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10010
        if( aop(bu,1001,5) < aop(bu,1005,5) ):
            if not( aop(bu,1012,5) == aop(bu,1005,5)-aop(bu,1001,5) ):
                lzbir =  aop(bu,1012,5) 
                dzbir =  aop(bu,1005,5)-aop(bu,1001,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1012 kol. 5 = AOP-u (1005 - 1001) kol. 5, ako je AOP 1001 kol. 5 < AOP-a 1005 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10011
        if( aop(bu,1001,6) < aop(bu,1005,6) ):
            if not( aop(bu,1012,6) == aop(bu,1005,6)-aop(bu,1001,6) ):
                lzbir =  aop(bu,1012,6) 
                dzbir =  aop(bu,1005,6)-aop(bu,1001,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1012 kol. 6 = AOP-u (1005 - 1001) kol. 6, ako je AOP 1001 kol. 6 < AOP-a 1005 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10012
        if( aop(bu,1001,5) == aop(bu,1005,5) ):
            if not( suma(bu,1011,1012,5) == 0 ):
                lzbir =  suma(bu,1011,1012,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1011 + 1012) kol. 5 = 0, ako je AOP 1001 kol. 5 = AOP-u 1005 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10013
        if( aop(bu,1001,6) == aop(bu,1005,6) ):
            if not( suma(bu,1011,1012,6) == 0 ):
                lzbir =  suma(bu,1011,1012,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1011 + 1012) kol. 6 = 0, ako je AOP 1001 kol. 6 = AOP-u 1005 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10014
        if( aop(bu,1011,5) > 0 ):
            if not( aop(bu,1012,5) == 0 ):
                lzbir =  aop(bu,1012,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1011 kol. 5 > 0 onda je AOP 1012 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10015
        if( aop(bu,1012,5) > 0 ):
            if not( aop(bu,1011,5) == 0 ):
                lzbir =  aop(bu,1011,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1012 kol. 5 > 0 onda je AOP 1011 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10016
        if( aop(bu,1011,6) > 0 ):
            if not( aop(bu,1012,6) == 0 ):
                lzbir =  aop(bu,1012,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1011 kol. 6 > 0 onda je AOP 1012 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10017
        if( aop(bu,1012,6) > 0 ):
            if not( aop(bu,1011,6) == 0 ):
                lzbir =  aop(bu,1011,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1012 kol. 6 > 0 onda je AOP 1011 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10018
        if not( suma_liste(bu,[1001,1012],5) == suma_liste(bu,[1005,1011],5) ):
            lzbir =  suma_liste(bu,[1001,1012],5) 
            dzbir =  suma_liste(bu,[1005,1011],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1012) kol. 5 = AOP-u (1005 + 1011) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10019
        if not( suma_liste(bu,[1001,1012],6) == suma_liste(bu,[1005,1011],6) ):
            lzbir =  suma_liste(bu,[1001,1012],6) 
            dzbir =  suma_liste(bu,[1005,1011],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1001 + 1012) kol. 6 = AOP-u (1005 + 1011) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10020
        if( aop(bu,1013,5) > aop(bu,1014,5) ):
            if not( aop(bu,1015,5) == aop(bu,1013,5)-aop(bu,1014,5) ):
                lzbir =  aop(bu,1015,5) 
                dzbir =  aop(bu,1013,5)-aop(bu,1014,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1015 kol. 5 = AOP-u (1013 - 1014) kol. 5, ako je AOP 1013 kol. 5 > AOP-a 1014 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10021
        if( aop(bu,1013,6) > aop(bu,1014,6) ):
            if not( aop(bu,1015,6) == aop(bu,1013,6)-aop(bu,1014,6) ):
                lzbir =  aop(bu,1015,6) 
                dzbir =  aop(bu,1013,6)-aop(bu,1014,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1015 kol. 6 = AOP-u (1013 - 1014) kol. 6, ako je AOP 1013 kol. 6 > AOP-a 1014 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10022
        if( aop(bu,1013,5) < aop(bu,1014,5) ):
            if not( aop(bu,1016,5) == aop(bu,1014,5)-aop(bu,1013,5) ):
                lzbir =  aop(bu,1016,5) 
                dzbir =  aop(bu,1014,5)-aop(bu,1013,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1016 kol. 5 = AOP-u (1014 - 1013) kol. 5, ako je AOP 1013 kol. 5 < AOP-a 1014 kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10023
        if( aop(bu,1013,6) < aop(bu,1014,6) ):
            if not( aop(bu,1016,6) == aop(bu,1014,6)-aop(bu,1013,6) ):
                lzbir =  aop(bu,1016,6) 
                dzbir =  aop(bu,1014,6)-aop(bu,1013,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1016 kol. 6 = AOP-u (1014 - 1013) kol. 6, ako je AOP 1013 kol. 6 < AOP-a 1014 kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10024
        if( aop(bu,1013,5) == aop(bu,1014,5) ):
            if not( suma(bu,1015,1016,5) == 0 ):
                lzbir =  suma(bu,1015,1016,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1015 + 1016) kol. 5 = 0, ako je AOP 1013 kol. 5 = AOP-u 1014 kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10025
        if( aop(bu,1013,6) == aop(bu,1014,6) ):
            if not( suma(bu,1015,1016,6) == 0 ):
                lzbir =  suma(bu,1015,1016,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1015 + 1016) kol. 6 = 0, ako je AOP 1013 kol. 6 = AOP-u 1014 kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10026
        if( aop(bu,1015,5) > 0 ):
            if not( aop(bu,1016,5) == 0 ):
                lzbir =  aop(bu,1016,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1015 kol. 5 > 0 onda je AOP 1016 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10027
        if( aop(bu,1016,5) > 0 ):
            if not( aop(bu,1015,5) == 0 ):
                lzbir =  aop(bu,1015,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1016 kol. 5 > 0 onda je AOP 1015 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10028
        if( aop(bu,1015,6) > 0 ):
            if not( aop(bu,1016,6) == 0 ):
                lzbir =  aop(bu,1016,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1015 kol. 6 > 0 onda je AOP 1016 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10029
        if( aop(bu,1016,6) > 0 ):
            if not( aop(bu,1015,6) == 0 ):
                lzbir =  aop(bu,1015,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1016 kol. 6 > 0 onda je AOP 1015 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10030
        if not( suma_liste(bu,[1013,1016],5) == suma(bu,1014,1015,5) ):
            lzbir =  suma_liste(bu,[1013,1016],5) 
            dzbir =  suma(bu,1014,1015,5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1013 + 1016) kol. 5 = AOP-u (1014 + 1015) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10031
        if not( suma_liste(bu,[1013,1016],6) == suma(bu,1014,1015,6) ):
            lzbir =  suma_liste(bu,[1013,1016],6) 
            dzbir =  suma(bu,1014,1015,6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1013 + 1016) kol. 6 = AOP-u (1014 + 1015) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10032
        if( aop(bu,1017,5) > 0 ):
            if not( aop(bu,1018,5) == 0 ):
                lzbir =  aop(bu,1018,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1017 kol. 5 > 0 onda je AOP 1018 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10033
        if( aop(bu,1018,5) > 0 ):
            if not( aop(bu,1017,5) == 0 ):
                lzbir =  aop(bu,1017,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1018 kol. 5 > 0 onda je AOP 1017 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10034
        if( aop(bu,1017,6) > 0 ):
            if not( aop(bu,1018,6) == 0 ):
                lzbir =  aop(bu,1018,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1017 kol. 6 > 0 onda je AOP 1018 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10035
        if( aop(bu,1018,6) > 0 ):
            if not( aop(bu,1017,6) == 0 ):
                lzbir =  aop(bu,1017,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1018 kol. 6 > 0 onda je AOP 1017 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10036
        if( aop(bu,1021,5) > 0 ):
            if not( aop(bu,1022,5) == 0 ):
                lzbir =  aop(bu,1022,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1021 kol. 5 > 0 onda je AOP 1022 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10037
        if( aop(bu,1022,5) > 0 ):
            if not( aop(bu,1021,5) == 0 ):
                lzbir =  aop(bu,1021,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1022 kol. 5 > 0 onda je AOP 1021 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10038
        if( aop(bu,1021,6) > 0 ):
            if not( aop(bu,1022,6) == 0 ):
                lzbir =  aop(bu,1022,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1021 kol. 6 > 0 onda je AOP 1022 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10039
        if( aop(bu,1022,6) > 0 ):
            if not( aop(bu,1021,6) == 0 ):
                lzbir =  aop(bu,1021,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1022 kol. 6 > 0 onda je AOP 1021 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10040
        if( suma_liste(bu,[1011,1015,1017,1019,1021],5) > suma_liste(bu,[1012,1016,1018,1020,1022],5) ):
            if not( aop(bu,1023,5) == suma_liste(bu,[1011,1015,1017,1019,1021],5)-suma_liste(bu,[1012,1016,1018,1020,1022],5) ):
                lzbir =  aop(bu,1023,5) 
                dzbir =  suma_liste(bu,[1011,1015,1017,1019,1021],5)-suma_liste(bu,[1012,1016,1018,1020,1022],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1023 kol. 5 = AOP-u (1011 - 1012 + 1015 - 1016 + 1017 - 1018 + 1019 - 1020 + 1021 - 1022) kol. 5, ako je AOP (1011 + 1015 + 1017 + 1019 + 1021) kol. 5 > AOP-a (1012 + 1016 + 1018 + 1020 + 1022) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10041
        if( suma_liste(bu,[1011,1015,1017,1019,1021],6) > suma_liste(bu,[1012,1016,1018,1020,1022],6) ):
            if not( aop(bu,1023,6) == suma_liste(bu,[1011,1015,1017,1019,1021],6)-suma_liste(bu,[1012,1016,1018,1020,1022],6) ):
                lzbir =  aop(bu,1023,6) 
                dzbir =  suma_liste(bu,[1011,1015,1017,1019,1021],6)-suma_liste(bu,[1012,1016,1018,1020,1022],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1023 kol. 6 = AOP-u (1011 - 1012 + 1015 - 1016 + 1017 - 1018 + 1019 - 1020 + 1021 - 1022) kol. 6, ako je AOP (1011 + 1015 + 1017 + 1019 + 1021) kol. 6 > AOP-a (1012 + 1016 + 1018 + 1020 + 1022) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10042
        if( suma_liste(bu,[1011,1015,1017,1019,1021],5) < suma_liste(bu,[1012,1016,1018,1020,1022],5) ):
            if not( aop(bu,1024,5) == suma_liste(bu,[1012,1016,1018,1020,1022],5)-suma_liste(bu,[1011,1015,1017,1019,1021],5) ):
                lzbir =  aop(bu,1024,5) 
                dzbir =  suma_liste(bu,[1012,1016,1018,1020,1022],5)-suma_liste(bu,[1011,1015,1017,1019,1021],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1024 kol. 5 = AOP-u (1012 - 1011 + 1016 - 1015 + 1018 - 1017 + 1020 - 1019 + 1022 - 1021) kol. 5, ako je AOP (1011 + 1015 + 1017 + 1019 + 1021) kol. 5 < AOP-a (1012 + 1016 + 1018 + 1020 + 1022) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10043
        if( suma_liste(bu,[1011,1015,1017,1019,1021],6) < suma_liste(bu,[1012,1016,1018,1020,1022],6) ):
            if not( aop(bu,1024,6) == suma_liste(bu,[1012,1016,1018,1020,1022],6)-suma_liste(bu,[1011,1015,1017,1019,1021],6) ):
                lzbir =  aop(bu,1024,6) 
                dzbir =  suma_liste(bu,[1012,1016,1018,1020,1022],6)-suma_liste(bu,[1011,1015,1017,1019,1021],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1024 kol. 6 = AOP-u (1012 - 1011 + 1016 - 1015 + 1018 - 1017 + 1020 - 1019 + 1022 - 1021) kol. 6, ako je AOP (1011 + 1015 + 1017 + 1019 + 1021) kol. 6 < AOP-a (1012 + 1016 + 1018 + 1020 + 1022) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10044
        if( suma_liste(bu,[1011,1015,1017,1019,1021],5) == suma_liste(bu,[1012,1016,1018,1020,1022],5) ):
            if not( suma(bu,1023,1024,5) == 0 ):
                lzbir =  suma(bu,1023,1024,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1023 + 1024) kol. 5 = 0, ako je AOP (1011 + 1015 + 1017 + 1019 + 1021) kol. 5 = AOP-u (1012 + 1016 + 1018 + 1020 + 1022) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10045
        if( suma_liste(bu,[1011,1015,1017,1019,1021],6) == suma_liste(bu,[1012,1016,1018,1020,1022],6) ):
            if not( suma(bu,1023,1024,6) == 0 ):
                lzbir =  suma(bu,1023,1024,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1023 + 1024) kol. 6 = 0, ako je AOP (1011 + 1015 + 1017 + 1019 + 1021) kol. 6 = AOP-u (1012 + 1016 + 1018 + 1020 + 1022) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10046
        if( aop(bu,1023,5) > 0 ):
            if not( aop(bu,1024,5) == 0 ):
                lzbir =  aop(bu,1024,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1023 kol. 5 > 0 onda je AOP 1024 kol. 5 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10047
        if( aop(bu,1024,5) > 0 ):
            if not( aop(bu,1023,5) == 0 ):
                lzbir =  aop(bu,1023,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1024 kol. 5 > 0 onda je AOP 1023 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10048
        if( aop(bu,1023,6) > 0 ):
            if not( aop(bu,1024,6) == 0 ):
                lzbir =  aop(bu,1024,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1023 kol. 6 > 0 onda je AOP 1024 kol. 6 = 0  U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10049
        if( aop(bu,1024,6) > 0 ):
            if not( aop(bu,1023,6) == 0 ):
                lzbir =  aop(bu,1023,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1024 kol. 6 > 0 onda je AOP 1023 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10050
        if not( suma_liste(bu,[1011,1015,1017,1019,1021,1024],5) == suma_liste(bu,[1012,1016,1018,1020,1022,1023],5) ):
            lzbir =  suma_liste(bu,[1011,1015,1017,1019,1021,1024],5) 
            dzbir =  suma_liste(bu,[1012,1016,1018,1020,1022,1023],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1011 + 1015 + 1017 + 1019 + 1021 + 1024) kol. 5 = AOP-u (1012 + 1016 + 1018 + 1020 + 1022 + 1023) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10051
        if not( suma_liste(bu,[1011,1015,1017,1019,1021,1024],6) == suma_liste(bu,[1012,1016,1018,1020,1022,1023],6) ):
            lzbir =  suma_liste(bu,[1011,1015,1017,1019,1021,1024],6) 
            dzbir =  suma_liste(bu,[1012,1016,1018,1020,1022,1023],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1011 + 1015 + 1017 + 1019 + 1021 + 1024) kol. 6 = AOP-u (1012 + 1016 + 1018 + 1020 + 1022 + 1023) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10052
        if not( aop(bu,1025,5) > 0 ):
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP 1025 kol. 5 > 0 Na poziciji Poreski rashod perioda nije iskazan podatak; Ukoliko podaci nisu prikazani, zakonski zastupnik svojim potpisom potvrđuje ispravnost toga '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_warnings.append(poruka_obrasca)
        
        #10053
        if( suma_liste(bu,[1023,1027],5) > suma(bu,1024,1026,5) ):
            if not( aop(bu,1028,5) == suma_liste(bu,[1023,1027],5)-suma(bu,1024,1026,5) ):
                lzbir =  aop(bu,1028,5) 
                dzbir =  suma_liste(bu,[1023,1027],5)-suma(bu,1024,1026,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1028 kol. 5 = AOP-u (1023 - 1024 - 1025 - 1026 + 1027) kol. 5, ako je AOP (1023 + 1027) kol. 5 > AOP-a (1024 + 1025 + 1026) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10054
        if( suma_liste(bu,[1023,1027],6) > suma(bu,1024,1026,6) ):
            if not( aop(bu,1028,6) == suma_liste(bu,[1023,1027],6)-suma(bu,1024,1026,6) ):
                lzbir =  aop(bu,1028,6) 
                dzbir =  suma_liste(bu,[1023,1027],6)-suma(bu,1024,1026,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1028 kol. 6 = AOP-u (1023 - 1024 - 1025 - 1026 + 1027) kol. 6, ako je AOP (1023 + 1027) kol. 6 > AOP-a (1024 + 1025 + 1026) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10055
        if( suma_liste(bu,[1023,1027],5) < suma(bu,1024,1026,5) ):
            if not( aop(bu,1029,5) == suma(bu,1024,1026,5)-suma_liste(bu,[1023,1027],5) ):
                lzbir =  aop(bu,1029,5) 
                dzbir =  suma(bu,1024,1026,5)-suma_liste(bu,[1023,1027],5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1029 kol. 5 = AOP-u (1024 - 1023 + 1025 + 1026 - 1027) kol. 5,  ako je AOP (1023 + 1027) kol. 5 < AOP-a (1024 + 1025 + 1026) kol. 5  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10056
        if( suma_liste(bu,[1023,1027],6) < suma(bu,1024,1026,6) ):
            if not( aop(bu,1029,6) == suma(bu,1024,1026,6)-suma_liste(bu,[1023,1027],6) ):
                lzbir =  aop(bu,1029,6) 
                dzbir =  suma(bu,1024,1026,6)-suma_liste(bu,[1023,1027],6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP 1029 kol. 6 = AOP-u (1024 - 1023 + 1025 + 1026 - 1027) kol. 6,  ako je AOP (1023 + 1027) kol. 6 < AOP-a (1024 + 1025 + 1026) kol. 6  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10057
        if( suma_liste(bu,[1023,1027],5) == suma(bu,1024,1026,5) ):
            if not( suma(bu,1028,1029,5) == 0 ):
                lzbir =  suma(bu,1028,1029,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1028 + 1029) kol. 5 = 0,  ako je AOP (1023 + 1027) kol. 5 = AOP-u (1024 + 1025 + 1026) kol. 5 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10058
        if( suma_liste(bu,[1023,1027],6) == suma(bu,1024,1026,6) ):
            if not( suma(bu,1028,1029,6) == 0 ):
                lzbir =  suma(bu,1028,1029,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='AOP (1028 + 1029) kol. 6 = 0,  ako je AOP (1023 + 1027) kol. 6 = AOP-u (1024 + 1025 + 1026) kol. 6 Rezultat mora biti jednak 0 ukoliko su pozitivne i odbitne stavke međusobno jednake '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10059
        if( aop(bu,1028,5) > 0 ):
            if not( aop(bu,1029,5) == 0 ):
                lzbir =  aop(bu,1029,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1028 kol. 5 > 0 onda je AOP 1029 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10060
        if( aop(bu,1029,5) > 0 ):
            if not( aop(bu,1028,5) == 0 ):
                lzbir =  aop(bu,1028,5) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1029 kol. 5 > 0 onda je AOP 1028 kol. 5 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10061
        if( aop(bu,1028,6) > 0 ):
            if not( aop(bu,1029,6) == 0 ):
                lzbir =  aop(bu,1029,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1028 kol. 6 > 0 onda je AOP 1029 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10062
        if( aop(bu,1029,6) > 0 ):
            if not( aop(bu,1028,6) == 0 ):
                lzbir =  aop(bu,1028,6) 
                dzbir =  0 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1029 kol. 6 > 0 onda je AOP 1028 kol. 6 = 0 U Bilansu uspeha ne mogu biti istovremeno prikazani dobitak i gubitak '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_errors.append(poruka_obrasca)
        
        #10063
        if not( suma_liste(bu,[1023,1027,1029],5) == suma_liste(bu,[1024,1025,1026,1028],5) ):
            lzbir =  suma_liste(bu,[1023,1027,1029],5) 
            dzbir =  suma_liste(bu,[1024,1025,1026,1028],5) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1023 + 1027 + 1029) kol. 5 = AOP-u (1024 + 1025 + 1026 + 1028) kol. 5 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10064
        if not( suma_liste(bu,[1023,1027,1029],6) == suma_liste(bu,[1024,1025,1026,1028],6) ):
            lzbir =  suma_liste(bu,[1023,1027,1029],6) 
            dzbir =  suma_liste(bu,[1024,1025,1026,1028],6) 
            razlika = lzbir - dzbir
            
            naziv_obrasca='Bilans uspeha'
            poruka  ='AOP (1023 + 1027 + 1029) kol. 6 = AOP-u (1024 + 1025 + 1026 + 1028) kol. 6 Kontrolno pravilo odražava princip bilansne ravnoteže; Proverite prethodno nezadovoljena kontrolna pravila i izvršite neophodne ispravke '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
            aop_pozicije=[]
            poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
            form_errors.append(poruka_obrasca)
        
        #10065
        if( aop(bu,1028,5) > 0 ):
            if not( aop(bs,411,5) == aop(bu,1028,5) ):
                lzbir =  aop(bs,411,5) 
                dzbir =  aop(bu,1028,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1028 kol. 5 > 0, onda je AOP 0411 kol. 5 bilansa stanja = AOP-u 1028 kol. 5   Neto dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu neraspoređenog dobitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1028 kol. 5 > 0, onda je AOP 0411 kol. 5 bilansa stanja = AOP-u 1028 kol. 5   Neto dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu neraspoređenog dobitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10066
        if( aop(bu,1028,6) > 0 ):
            if not( aop(bs,411,6) == aop(bu,1028,6) ):
                lzbir =  aop(bs,411,6) 
                dzbir =  aop(bu,1028,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1028 kol. 6  > 0, onda je AOP 0411 kol. 6 bilansa stanja = AOP-u 1028 kol. 6   Neto dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak   neraspoređenom dobitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1028 kol. 6  > 0, onda je AOP 0411 kol. 6 bilansa stanja = AOP-u 1028 kol. 6   Neto dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak   neraspoređenom dobitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10067
        if( aop(bs,411,5) > 0 ):
            if not( aop(bu,1028,5) == aop(bs,411,5) ):
                lzbir =  aop(bu,1028,5) 
                dzbir =  aop(bs,411,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0411 kol. 5 bilansa stanja > 0, onda je AOP 1028 kol. 5  = AOP-u 0411 kol. 5 bilansa stanja  Neto dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu neraspoređenog dobitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 0411 kol. 5 bilansa stanja > 0, onda je AOP 1028 kol. 5  = AOP-u 0411 kol. 5 bilansa stanja  Neto dobitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu neraspoređenog dobitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10068
        if( aop(bs,411,6) > 0 ):
            if not( aop(bu,1028,6) == aop(bs,411,6) ):
                lzbir =  aop(bu,1028,6) 
                dzbir =  aop(bs,411,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0411 kol. 6 bilansa stanja > 0, onda je AOP 1028 kol. 6  = AOP-u 0411 kol. 6 bilansa stanja  Neto dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak   neraspoređenom dobitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 0411 kol. 6 bilansa stanja > 0, onda je AOP 1028 kol. 6  = AOP-u 0411 kol. 6 bilansa stanja  Neto dobitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak   neraspoređenom dobitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10069
        if( aop(bu,1029,5) > 0 ):
            if not( aop(bs,414,5) == aop(bu,1029,5) ):
                lzbir =  aop(bs,414,5) 
                dzbir =  aop(bu,1029,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1029 kol. 5 > 0, onda  je AOP 0414 kol. 5 bilansa stanja = AOP-u 1029 kol. 5  Neto gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu gubitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1029 kol. 5 > 0, onda  je AOP 0414 kol. 5 bilansa stanja = AOP-u 1029 kol. 5  Neto gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu gubitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10070
        if( aop(bu,1029,6) > 0 ):
            if not( aop(bs,414,6) == aop(bu,1029,6) ):
                lzbir =  aop(bs,414,6) 
                dzbir =  aop(bu,1029,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 1029 kol. 6  > 0, onda  je AOP 0414 kol. 6 bilansa stanja = AOP-u 1029 kol. 6  Neto gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak  gubitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 1029 kol. 6  > 0, onda  je AOP 0414 kol. 6 bilansa stanja = AOP-u 1029 kol. 6  Neto gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak  gubitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10071
        if( aop(bs,414,5) > 0 ):
            if not( aop(bu,1029,5) == aop(bs,414,5) ):
                lzbir =  aop(bu,1029,5) 
                dzbir =  aop(bs,414,5) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0414 kol. 5 bilansa stanja > 0, onda je AOP 1029 kol. 5 = AOP-u 0414 kol. 5 bilansa stanja Neto gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu gubitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 0414 kol. 5 bilansa stanja > 0, onda je AOP 1029 kol. 5 = AOP-u 0414 kol. 5 bilansa stanja Neto gubitak tekuće godine u obrascu Bilans uspeha, po pravilu, mora biti jednak iznosu gubitka tekuće godine u obrascu Bilans stanja; Potrebno je u delu "Dokumentacija", pod "Ostalo" dostaviti Obrazloženje nastalih razlika; U suprotnom, obvezniku će biti poslato Obaveštenje o nedostacima. '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
        
        #10072
        if( aop(bs,414,6) > 0 ):
            if not( aop(bu,1029,6) == aop(bs,414,6) ):
                lzbir =  aop(bu,1029,6) 
                dzbir =  aop(bs,414,6) 
                razlika = lzbir - dzbir
                
                naziv_obrasca='Bilans stanja'
                poruka  ='Ako je AOP 0414 kol. 6 bilansa stanja > 0, onda je AOP 1029 kol. 6 = AOP-u 0414 kol. 6 bilansa stanja Neto gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak  gubitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
                aop_pozicije=[]
                poruka_obrasca = {'naziv_obrasca': naziv_obrasca, 'poruka': poruka, 'aop_pozicije': aop_pozicije}
                form_warnings.append(poruka_obrasca)
                naziv_obrasca='Bilans uspeha'
                poruka  ='Ako je AOP 0414 kol. 6 bilansa stanja > 0, onda je AOP 1029 kol. 6 = AOP-u 0414 kol. 6 bilansa stanja Neto gubitak prethodne godine u obrascu Bilans uspeha, po pravilu, mora biti jednak  gubitku tekuće godine iskazanom u koloni prethodna godina u obrascu Bilans stanja.  '+'(Levi zbir = '+'' +str(lzbir)+ ''+', Desni zbir = '+'' +str(dzbir)+ ''+', Razlika = '+'' +str(razlika)+ ''+') '
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

