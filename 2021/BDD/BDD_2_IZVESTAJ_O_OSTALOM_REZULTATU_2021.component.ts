import { ChangeDetectorRef, Component } from '@angular/core'
import { Obrazac } from "../../obrazac";
import { BackendServiceService } from "../../../backend-service.service";

@Component({
  selector: 'BDD_2_IZVESTAJ_O_OSTALOM_REZULTATU_2021',
  templateUrl: 'BDD_2_IZVESTAJ_O_OSTALOM_REZULTATU_2021.component.html',
})
export class BDD_2_IZVESTAJ_O_OSTALOM_REZULTATU_2021 extends Obrazac {

  constructor(_backendService: BackendServiceService,
    _cd: ChangeDetectorRef) {
    super(_backendService, _cd);
  }
}
